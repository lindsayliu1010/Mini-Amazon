from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .purchases import bp as purchase_bp
    app.register_blueprint(purchase_bp)
    
    from .wishlist import bp as wishlist_bp
    app.register_blueprint(wishlist_bp)

    from .product import bp as products_bp
    app.register_blueprint(products_bp)

    from .cart import bp as cart_bp
    app.register_blueprint(cart_bp)

    return app
