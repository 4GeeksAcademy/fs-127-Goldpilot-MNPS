import os
import requests as req
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db
from api.models.wallet import MetaApiAccount

wallet_bp = Blueprint('wallet', __name__, url_prefix='/wallets')

METAAPI_BASE_URL = "https://mt-provisioning-api-v1.agiliumtrade.agiliumtrade.ai"
METAAPI_PROVISIONING_URL = f"{METAAPI_BASE_URL}/users/current/accounts"
METAAPI_CLIENT_BASE = "https://mt-client-api-v1.{region}.agiliumtrade.ai"


def _metaapi_headers():
    token = os.getenv("META_API_TOKEN", os.getenv("METAAPI_TOKEN", ""))
    return {"auth-token": token, "Content-Type": "application/json"}


def _check_token():
    token = os.getenv("META_API_TOKEN", os.getenv("METAAPI_TOKEN", ""))
    return token and token != "your_metaapi_token_here"


@wallet_bp.route('/servers', methods=['GET'])
@jwt_required()
def search_servers():
    """
    Proxy to MetaApi known-servers search.
    Query params: query (string), platform (mt4|mt5)
    Returns: { servers: { "Broker Name": ["Server1", "Server2"], ... } }
    """
    query = request.args.get("query", "").strip()
    platform = request.args.get("platform", "mt4").strip().lower()
    version = 5 if platform == "mt5" else 4

    if not query:
        return jsonify({"servers": {}}), 200

    if not _check_token():
        return jsonify({"servers": {}}), 200

    try:
        resp = req.get(
            f"{METAAPI_BASE_URL}/known-mt-servers/{version}/search",
            params={"query": query},
            headers={"auth-token": os.getenv("METAAPI_TOKEN", "")},
            timeout=10,
        )
        if resp.ok:
            return jsonify({"servers": resp.json()}), 200
    except Exception:
        pass

    return jsonify({"servers": {}}), 200


def _sync_account_status(account):
    """
    Calls MetaApi to check the current state of a DRAFT account.
    Updates status and login in DB if the account is now deployed/connected.
    Returns True if the status was updated.
    """
    try:
        resp = req.get(
            f"{METAAPI_PROVISIONING_URL}/{account.account_id}",
            headers=_metaapi_headers(),
            timeout=10,
        )
        if not resp.ok:
            return False
        data = resp.json()
        state = data.get("state", "").upper()
        region_val = data.get("region")
        if region_val:
            account.region = region_val
        # DEPLOYED means MetaApi is syncing the account with the broker
        if state in ("DEPLOYED", "DEPLOYING", "CONNECTED"):
            account.status = "connected"
            login_val = data.get("login")
            if login_val:
                account.login = str(login_val)
            db.session.commit()
            return True
        elif region_val:
            db.session.commit()
    except Exception:
        pass
    return False


@wallet_bp.route('', methods=['GET'])
@jwt_required()
def get_wallets():
    """
    Returns all MetaApi accounts for the current user.
    Automatically syncs status for any accounts still in DRAFT state
    (i.e. the user completed the config-link flow on MetaApi's page).
    """
    user_id = int(get_jwt_identity())
    accounts = MetaApiAccount.query.filter_by(user_id=user_id).all()

    if _check_token():
        for account in accounts:
            if account.status == "draft" or not account.region:
                _sync_account_status(account)

    return jsonify({"wallets": [a.serialize() for a in accounts]}), 200


@wallet_bp.route('', methods=['POST'])
@jwt_required()
def add_wallet():
    """
    Creates a new MetaApi account in DRAFT state under the admin's subscription.
    Returns a configuration link — user enters MT credentials on MetaApi's secure page.
    MT password never touches our server.
    """
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    server = data.get("server", "").strip()
    platform = data.get("platform", "mt4").strip().lower()
    name = data.get("name", "").strip() or f"GoldPilot-{server}"
    account_type = data.get("account_type", "demo").strip()

    if not server:
        return jsonify({"description": "server es obligatorio"}), 400

    if platform not in ("mt4", "mt5"):
        return jsonify({"description": "platform debe ser mt4 o mt5"}), 400

    if not _check_token():
        return jsonify({"description": "METAAPI_TOKEN no configurado en el servidor"}), 503

    # Create account in DRAFT state — no credentials, returns instantly
    payload = {
        "name": name,
        "server": server,
        "platform": platform,
        "magic": 0,
        "type": "cloud-g2",
    }

    try:
        resp = req.post(
            METAAPI_PROVISIONING_URL,
            json=payload,
            headers=_metaapi_headers(),
            timeout=15,
        )
    except req.exceptions.RequestException as e:
        return jsonify({"description": f"Error al conectar con MetaApi: {str(e)}"}), 502

    if not resp.ok:
        try:
            error_detail = resp.json().get("message", resp.text)
        except Exception:
            error_detail = resp.text
        return jsonify({"description": f"MetaApi error: {error_detail}"}), resp.status_code

    resp_data = resp.json()
    meta_account_id = resp_data.get("id")
    if not meta_account_id:
        return jsonify({"description": "MetaApi no retornó un account ID"}), 502
    meta_region = resp_data.get("region")

    # Request a configuration link for the user to enter MT credentials securely
    config_link = ""
    try:
        link_resp = req.put(
            f"{METAAPI_PROVISIONING_URL}/{meta_account_id}/configuration-link",
            headers=_metaapi_headers(),
            timeout=15,
        )
        if link_resp.ok:
            config_link = link_resp.json().get("configurationLink", "")
    except Exception:
        pass

    account = MetaApiAccount(
        user_id=user_id,
        account_id=meta_account_id,
        server=server,
        platform=platform,
        broker_name=name,
        account_type=account_type,
        status="draft",
        region=meta_region,
    )
    db.session.add(account)
    db.session.commit()

    return jsonify({
        "msg": "Cuenta creada. Usa el enlace de configuración para ingresar tus credenciales MT.",
        "wallet": account.serialize(),
        "configuration_link": config_link,
    }), 200


@wallet_bp.route('/<int:wallet_id>/sync', methods=['POST'])
@jwt_required()
def sync_wallet(wallet_id):
    """Manually syncs a wallet's status with MetaApi and returns the updated wallet."""
    user_id = int(get_jwt_identity())
    account = MetaApiAccount.query.filter_by(id=wallet_id, user_id=user_id).first()
    if not account:
        return jsonify({"description": "Wallet no encontrada"}), 404

    if not _check_token():
        return jsonify({"description": "METAAPI_TOKEN no configurado en el servidor"}), 503

    _sync_account_status(account)
    return jsonify({"wallet": account.serialize()}), 200


@wallet_bp.route('/<int:wallet_id>/config-link', methods=['GET'])
@jwt_required()
def get_config_link(wallet_id):
    """Returns a fresh MetaApi configuration link for a specific wallet."""
    user_id = int(get_jwt_identity())
    account = MetaApiAccount.query.filter_by(id=wallet_id, user_id=user_id).first()
    if not account:
        return jsonify({"description": "Wallet no encontrada"}), 404

    if not _check_token():
        return jsonify({"description": "METAAPI_TOKEN no configurado en el servidor"}), 503

    try:
        link_resp = req.put(
            f"{METAAPI_PROVISIONING_URL}/{account.account_id}/configuration-link",
            headers=_metaapi_headers(),
            timeout=15,
        )
        if not link_resp.ok:
            return jsonify({"description": "MetaApi no pudo generar el enlace"}), 502
        config_link = link_resp.json().get("configurationLink", "")
        return jsonify({"configuration_link": config_link}), 200
    except req.exceptions.RequestException as e:
        return jsonify({"description": f"Error al conectar con MetaApi: {str(e)}"}), 502


@wallet_bp.route('/<int:wallet_id>/balance', methods=['GET'])
@jwt_required()
def get_wallet_balance(wallet_id):
    """
    Fetches live balance/equity from MetaApi's client REST API.
    Requires the account to be DEPLOYED and CONNECTED to the broker.
    Returns null values if unavailable (draft, disconnected, or error).
    """
    user_id = int(get_jwt_identity())
    account = MetaApiAccount.query.filter_by(id=wallet_id, user_id=user_id).first()
    if not account:
        return jsonify({"description": "Wallet no encontrada"}), 404

    empty = {"balance": None, "equity": None, "currency": None, "margin": None, "free_margin": None}

    if account.status != "connected":
        return jsonify(empty), 200

    # Populate region for wallets created before region support was added
    if not account.region and _check_token():
        _sync_account_status(account)

    if not account.region:
        return jsonify(empty), 200

    try:
        base = METAAPI_CLIENT_BASE.format(region=account.region)
        resp = req.get(
            f"{base}/users/current/accounts/{account.account_id}/account-information",
            headers=_metaapi_headers(),
            timeout=10,
        )
        if resp.ok:
            d = resp.json()
            return jsonify({
                "balance": d.get("balance"),
                "equity": d.get("equity"),
                "currency": d.get("currency", "USD"),
                "margin": d.get("margin"),
                "free_margin": d.get("freeMargin"),
            }), 200
    except Exception:
        pass

    return jsonify(empty), 200


@wallet_bp.route('/<int:wallet_id>', methods=['DELETE'])
@jwt_required()
def delete_wallet(wallet_id):
    """Removes a specific wallet from MetaApi and the DB."""
    user_id = int(get_jwt_identity())
    account = MetaApiAccount.query.filter_by(id=wallet_id, user_id=user_id).first()
    if not account:
        return jsonify({"description": "Wallet no encontrada"}), 404

    # Remove from MetaApi (best effort)
    try:
        req.delete(
            f"{METAAPI_PROVISIONING_URL}/{account.account_id}",
            headers=_metaapi_headers(),
            timeout=15,
        )
    except Exception:
        pass

    db.session.delete(account)
    db.session.commit()
    return jsonify({"msg": "Wallet desconectada"}), 200
