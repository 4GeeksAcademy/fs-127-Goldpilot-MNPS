import asyncio
from dotenv import load_dotenv
import os
from metaapi_cloud_sdk import MetaApi

# Cargamos las variables del .env
load_dotenv()

async def probar_disparo():
    token = os.getenv("METAAPI_TOKEN")
    account_id = os.getenv("METAAPI_ACCOUNT_ID")
    
    print("Iniciando conexión con MetaApi...")
    api = MetaApi(token)
    
    try:
        account = await api.metatrader_account_api.get_account(account_id)
        if account.state not in ['DEPLOYING', 'DEPLOYED']:
            print("Desplegando cuenta...")
            await account.deploy()
        
        await account.wait_connected()
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        print("Conectado a MT5. ¡Disparando orden de prueba (0.01 Lotes ORO)...!")
        
        # Ojo: El símbolo del oro en MetaQuotes-Demo es XAUUSD.
        result = await connection.create_market_buy_order(
            "XAUUSD", 
            0.01, 
            0.0, # Sin SL
            0.0, # Sin TP
            {'comment': 'Prueba GoldPilot'}
        )
        
        print(f"✅ ¡ÉXITO! Orden ejecutada. ID: {result['orderId']}")
        
    except Exception as e:
        print(f"❌ Error al disparar: {e}")

# Ejecutamos
asyncio.run(probar_disparo())