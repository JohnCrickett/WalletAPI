from wallet_api import create_app

# As of gunicorn 20.x it can no longer call create_app() directly
app = create_app()
