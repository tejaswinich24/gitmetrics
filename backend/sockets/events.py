import eventlet
from datetime import datetime
from flask_socketio import join_room, leave_room, emit
from extensions import socketio, db
from github_client import get_user_events
from models import CachedEvent
from config import POLL_INTERVAL_SECONDS

active_rooms = {}  # username -> True while someone is watching

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

@socketio.on("watch_user")
def handle_watch(data):
    username = data.get("username")
    if not username:
        return
    join_room(username)
    emit("watch_ack", {"username": username, "status": "watching"})

    if username not in active_rooms:
        active_rooms[username] = True
        socketio.start_background_task(poll_loop, username)
        print(f"Started polling for: {username}")

@socketio.on("unwatch_user")
def handle_unwatch(data):
    username = data.get("username")
    if not username:
        return
    leave_room(username)
    active_rooms.pop(username, None)
    print(f"Stopped polling for: {username}")


def poll_loop(username):
    from app import app  # needed to access app context inside background task

    while active_rooms.get(username):
        with app.app_context():
            try:
                events = get_user_events(username)
                new_events = []

                for e in events:
                    exists = CachedEvent.query.filter_by(github_event_id=e["id"]).first()
                    if not exists:
                        ce = CachedEvent(
                            username=username,
                            github_event_id=e["id"],
                            event_type=e["type"],
                            repo_name=e["repo"]["name"],
                            payload=e,
                        )
                        db.session.add(ce)
                        new_events.append({
                            "id": e["id"],
                            "type": e["type"],
                            "repo": e["repo"]["name"],
                            "created_at": e["created_at"],
                        })

                if new_events:
                    db.session.commit()
                    socketio.emit("new_events", new_events, room=username)
                    print(f"Pushed {len(new_events)} new event(s) for {username}")

            except Exception as ex:
                print(f"Poll error for {username}: {ex}")
                socketio.emit("poll_error", {"error": str(ex)}, room=username)

        eventlet.sleep(POLL_INTERVAL_SECONDS)