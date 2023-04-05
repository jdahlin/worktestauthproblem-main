"""Settings for the SSO server."""
import os

BASE_URL = "http://127.0.0.1:5000/"
JWT_ACCESS_TOKEN_LIFETIME = 60
JWT_REFRESH_TOKEN_LIFETIME = 3600 * 24
JWT_ALGORITHM = "ES256"
JWT_ISSUER = BASE_URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./sql_app_test.db"

if os.environ.get("TESTING"):
    DB_URL = SQLALCHEMY_DATABASE_TEST_URL
else:
    DB_URL = SQLALCHEMY_DATABASE_URL
