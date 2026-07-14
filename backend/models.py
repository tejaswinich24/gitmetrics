from extensions import db
from datetime import datetime

class CachedSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True, nullable=False)
    profile_json = db.Column(db.JSON)
    repos_json = db.Column(db.JSON)
    languages_json = db.Column(db.JSON)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

class CachedEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True)
    github_event_id = db.Column(db.String(64), unique=True)
    event_type = db.Column(db.String(64))
    repo_name = db.Column(db.String(255))
    payload = db.Column(db.JSON)
    github_created_at = db.Column(db.DateTime)  # NEW: GitHub's real event timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # when WE cached it (keep for debugging)