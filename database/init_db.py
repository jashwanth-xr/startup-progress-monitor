"""
Run this once to initialize the database and create all tables.
Usage: python database/init_db.py
"""
from database.connection import Base, engine
from models.startup import Startup    # noqa: F401 — must import so Base knows about it
from models.metrics import Metrics    # noqa: F401 — must import so Base knows about it


def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done! Tables created: startups, metrics")
    print("✅ startup_monitor.db is ready.")


if __name__ == "__main__":
    main()