
import click
from datetime import date
from api.models import db, User, Strategy

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):

    """
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass

    @app.cli.command("seed")
    def seed():
        """Seed the Supabase database with demo users and default strategies."""

        # --- Strategies ---
        strategies_data = [
            {
                "name": "Low Risk",
                "risk_level": "low",
                "description": "Conservative strategy with small lot sizes and wide stops.",
                "default_lot_size": 0.01,
                "default_stop_loss": 50,
                "default_take_profit": 100,
            },
            {
                "name": "Medium Risk",
                "risk_level": "medium",
                "description": "Balanced strategy for moderate risk tolerance.",
                "default_lot_size": 0.05,
                "default_stop_loss": 30,
                "default_take_profit": 60,
            },
            {
                "name": "High Risk",
                "risk_level": "high",
                "description": "Aggressive strategy with larger positions.",
                "default_lot_size": 0.10,
                "default_stop_loss": 20,
                "default_take_profit": 40,
            },
        ]

        for data in strategies_data:
            existing = Strategy.query.filter_by(name=data["name"]).first()
            if existing:
                print(f"  [skip] Strategy '{data['name']}' already exists.")
            else:
                strategy = Strategy(**data)
                db.session.add(strategy)
                print(f"  [+] Strategy '{data['name']}' created.")

        db.session.commit()

        # --- Demo Users ---
        demo_users = [
            {
                "email": "demo@goldpilot.com",
                "username": "demo_user",
                "password": "Demo1234!",
                "first_name": "Demo",
                "last_name": "User",
                "phone_number": "+1234567890",
                "birth_date": date(1995, 1, 1),
            },
            {
                "email": "tester@goldpilot.com",
                "username": "tester_user",
                "password": "Test1234!",
                "first_name": "Tester",
                "last_name": "User",
                "phone_number": "+0987654321",
                "birth_date": date(1995, 6, 15),
            },
        ]

        for data in demo_users:
            existing = User.query.filter_by(email=data["email"]).first()
            if existing:
                print(f"  [skip] User '{data['email']}' already exists.")
            else:
                password = data.pop("password")
                user = User(**data, is_active=True, is_verified=True)
                user.set_password(password)
                db.session.add(user)
                print(f"  [+] User '{data['email']}' created.")

        db.session.commit()
        print("\nSeed complete.")
        print("Demo credentials:")
        print("  demo@goldpilot.com    /  Demo1234!")
        print("  tester@goldpilot.com  /  Test1234!")