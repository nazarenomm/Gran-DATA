from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from services.veda import VedaService

db = SQLAlchemy()
jwt = JWTManager()
veda_service = VedaService()