import eventlet
eventlet.monkey_patch()
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db, socketio
from config import DATABASE_URL
from routes.user_routes import user_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/*": {"origins": "*"}})
db.init_app(app)
from models import CachedSummary, CachedEvent
migrate = Migrate(app, db)
socketio.init_app(app)

app.register_blueprint(user_bp, url_prefix="/api")

import sockets.events  # registers socket event handlers

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)