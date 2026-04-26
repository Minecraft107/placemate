from flask import Flask, render_template
from flask_cors import CORS
from config import Config

from extensions import db, jwt

# Blueprints
from routes.auth import auth_bp
from routes.resume import resume_bp
from routes.eligibility import eligibility_bp
from routes.predict import predict_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Debug DB connection
    print("DB URL:", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register API blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(resume_bp, url_prefix="/api/resume")
    app.register_blueprint(
        eligibility_bp,
        url_prefix="/api"
    )  # gives /api/companies and /api/eligibility/check
    app.register_blueprint(
        predict_bp,
        url_prefix="/api"
    )  # gives /api/predict

    # ---------------- FRONTEND ROUTES ----------------

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        # Import all models so SQLAlchemy registers them
        import models
        from models.company import Company

        # Create all tables automatically
        db.create_all()

        print("Tables:", db.metadata.tables.keys())

        # Seed company data only once
        if Company.query.count() == 0:
            companies = [
                Company(
                    name="TCS",
                    min_cgpa=6.5,
                    backlogs_allowed=2,
                    required_skills=["java", "sql"],
                    min_package=3.5,
                    eligible_branches="CSE,IT"
                ),
                Company(
                    name="Infosys",
                    min_cgpa=6.0,
                    backlogs_allowed=2,
                    required_skills=["python", "sql"],
                    min_package=3.2,
                    eligible_branches="CSE,IT,ECE"
                ),
                Company(
                    name="Google",
                    min_cgpa=8.0,
                    backlogs_allowed=0,
                    required_skills=["python", "ds", "algorithms"],
                    min_package=20,
                    eligible_branches="CSE"
                )
            ]

            db.session.add_all(companies)
            db.session.commit()

            print("Companies auto-inserted")

    app.run(debug=True)