"""
Quick sanity test — run this once to verify DB setup.
Usage: python test_db.py
"""
from database.connection import engine, SessionLocal, Base
from models.startup import Startup
from models.metrics import Metrics
from datetime import date

# 1. Create all tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created: startups, metrics")

# 2. Open a session
db = SessionLocal()

# 3. Insert a test startup
s = Startup(name="Zepto", sector="Quick Commerce", founding_year=2021, stage="Series D", website="zepto.com")
db.add(s)
db.commit()
db.refresh(s)
print(f"✅ Startup inserted: {s}")

# 4. Insert a test metric row
m = Metrics(
    startup_id=s.id,
    month=date(2024, 3, 1),
    monthly_users=500000,
    monthly_revenue=12000000.0,
    employee_count=340,
    funding_raised=200000000.0,
    burn_rate=8000000.0
)
db.add(m)
db.commit()
db.refresh(m)
print(f"✅ Metrics inserted: {m}")

# 5. Query back and verify relationship
fetched = db.query(Startup).filter(Startup.name == "Zepto").first()
print(f"✅ Queried startup: {fetched.name}, metrics count: {len(fetched.metrics)}")
print(f"   └─ Month: {fetched.metrics[0].month}, Revenue: ₹{fetched.metrics[0].monthly_revenue:,.0f}")

# 6. Cleanup test data
db.delete(fetched)
db.commit()
db.close()
print("✅ Cleanup done — DB is working perfectly!")