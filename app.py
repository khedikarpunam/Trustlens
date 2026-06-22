import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from models import db, User
from config import Config

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.resume_routes import resume_bp
from routes.analysis_routes import analysis_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(analysis_bp)

    # Setup database
    with app.app_context():
        # Ensure database folder exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
            
        db.create_all()

    # Route root to login / dashboard
    @app.route('/')
    def root():
        return redirect(url_for('dashboard.index'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)
