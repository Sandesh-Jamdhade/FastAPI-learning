from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from .database import SessionLocal
from .models import Show

scheduler = BackgroundScheduler()

def delete_expired_shows():

    db = SessionLocal()

    try:
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        expired_shows = db.query(Show).filter(Show.end_time < now).all()

        print(f"Scheduler running... Found {len(expired_shows)} expired shows")

        for show in expired_shows:
            db.delete(show)

        db.commit()

        print("Expired shows deleted")

    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(delete_expired_shows, "interval", minutes=1)
    scheduler.start()