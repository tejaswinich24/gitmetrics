from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from extensions import db
from models import CachedSummary, CachedEvent
from github_client import get_user_profile, get_user_repos, get_repo_languages, get_user_events

user_bp = Blueprint("user", __name__)

CACHE_TTL_MINUTES = 5
EVENTS_TTL_SECONDS = 20

_last_events_fetch = {}

@user_bp.route("/user/<username>/summary")
def user_summary(username):
    cached = CachedSummary.query.filter_by(username=username).first()

    if cached and datetime.utcnow() - cached.fetched_at < timedelta(minutes=CACHE_TTL_MINUTES):
        return jsonify({
            "profile": cached.profile_json,
            "repos": cached.repos_json,
            "languages": cached.languages_json,
            "cached": True,
            "fetched_at": cached.fetched_at.isoformat()
        })

    profile = get_user_profile(username)
    repos = get_user_repos(username)

    lang_totals = {}
    for r in repos:
        try:
            langs = get_repo_languages(username, r["name"])
            for lang, byte_count in langs.items():
                lang_totals[lang] = lang_totals.get(lang, 0) + byte_count
        except Exception:
            continue

    if cached:
        cached.profile_json = profile
        cached.repos_json = repos
        cached.languages_json = lang_totals
        cached.fetched_at = datetime.utcnow()
    else:
        cached = CachedSummary(
            username=username,
            profile_json=profile,
            repos_json=repos,
            languages_json=lang_totals,
            fetched_at=datetime.utcnow()
        )
        db.session.add(cached)

    db.session.commit()

    return jsonify({
        "profile": profile,
        "repos": repos,
        "languages": lang_totals,
        "cached": False,
        "fetched_at": cached.fetched_at.isoformat()
    })


@user_bp.route("/user/<username>/events")
def user_events(username):
    now = datetime.utcnow()
    last_fetch = _last_events_fetch.get(username)

    if not last_fetch or (now - last_fetch).total_seconds() > EVENTS_TTL_SECONDS:
        try:
            events = get_user_events(username)
            for e in events:
                exists = CachedEvent.query.filter_by(github_event_id=e["id"]).first()
                if not exists:
                    github_time = datetime.strptime(e["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    ce = CachedEvent(
                        username=username,
                        github_event_id=e["id"],
                        event_type=e["type"],
                        repo_name=e["repo"]["name"],
                        payload=e,
                        github_created_at=github_time,
                    )
                    db.session.add(ce)
            db.session.commit()
            _last_events_fetch[username] = now
        except Exception as ex:
            return jsonify({"error": str(ex)}), 500

    recent = (
        CachedEvent.query
        .filter_by(username=username)
        .order_by(CachedEvent.github_created_at.desc())
        .limit(30)
        .all()
    )

    return jsonify([
        {
            "id": e.github_event_id,
            "type": e.event_type,
            "repo": e.repo_name,
            "created_at": (e.github_created_at or e.created_at).isoformat() + "Z"
        }
        for e in recent
    ])