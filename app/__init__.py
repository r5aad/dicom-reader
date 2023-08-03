from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from .models.models import db
    with app.app_context():
        db.init_app(app)
        db.create_all()
        db.session.commit()
    from .routes.api import api_bp
    app.register_blueprint(api_bp)
    return app
