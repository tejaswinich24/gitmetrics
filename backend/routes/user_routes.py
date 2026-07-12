from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from extensions import db
from models import CachedSummary
from github_client import get_user_profile, get_user_repos, get_repo_languages

user_bp = Blueprint("user", __name__)

CACHE_TTL_MINUTES = 5

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

    # Cache miss or stale — fetch fresh from GitHub
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