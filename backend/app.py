from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from config import DATABASE_URL
from routes.user_routes import user_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/*": {"origins": "*"}})
db.init_app(app)
from models import CachedSummary, CachedEvent
migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix="/api")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)