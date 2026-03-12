from sqlalchemy.orm import Session
from database.connection import SessionLocal
from models.startup import Startup
from models.metrics import Metrics
from datetime import date


def seed():
    db: Session = SessionLocal()

    # skip if data already exists
    if db.query(Startup).count() > 0:
        print("⚠️  Seed data already exists — skipping.")
        db.close()
        return

    # ----- startups -----
    startups = [
        Startup(name="Zepto",    sector="Quick Commerce", founding_year=2021, stage="Series B", website="https://zepto.com"),
        Startup(name="Razorpay", sector="Fintech",        founding_year=2014, stage="Series D", website="https://razorpay.com"),
        Startup(name="CRED",     sector="Fintech",        founding_year=2018, stage="Series C", website="https://cred.club"),
        Startup(name="Groww",    sector="Fintech",        founding_year=2016, stage="Series D", website="https://groww.in"),
        Startup(name="Meesho",   sector="E-Commerce",     founding_year=2015, stage="Series E", website="https://meesho.com"),
    ]
    db.add_all(startups)
    db.commit()
    for s in startups:
        db.refresh(s)

    # ----- metrics -----
    metrics_data = [
        # Zepto — fast growth
        Metrics(startup_id=startups[0].id, month=date(2024,1,1), monthly_users=500000,  monthly_revenue=200000,  employee_count=300, funding_raised=20000000,  burn_rate=350000),
        Metrics(startup_id=startups[0].id, month=date(2024,2,1), monthly_users=650000,  monthly_revenue=260000,  employee_count=320, funding_raised=20000000,  burn_rate=380000),
        Metrics(startup_id=startups[0].id, month=date(2024,3,1), monthly_users=820000,  monthly_revenue=340000,  employee_count=345, funding_raised=20000000,  burn_rate=390000),

        # Razorpay — stable large startup
        Metrics(startup_id=startups[1].id, month=date(2024,1,1), monthly_users=2000000, monthly_revenue=900000,  employee_count=800, funding_raised=100000000, burn_rate=600000),
        Metrics(startup_id=startups[1].id, month=date(2024,2,1), monthly_users=2300000, monthly_revenue=980000,  employee_count=820, funding_raised=100000000, burn_rate=640000),
        Metrics(startup_id=startups[1].id, month=date(2024,3,1), monthly_users=2500000, monthly_revenue=1050000, employee_count=850, funding_raised=100000000, burn_rate=650000),

        # CRED — slowing down
        Metrics(startup_id=startups[2].id, month=date(2024,1,1), monthly_users=1500000, monthly_revenue=700000,  employee_count=600, funding_raised=80000000,  burn_rate=500000),
        Metrics(startup_id=startups[2].id, month=date(2024,2,1), monthly_users=1650000, monthly_revenue=760000,  employee_count=620, funding_raised=80000000,  burn_rate=540000),
        Metrics(startup_id=startups[2].id, month=date(2024,3,1), monthly_users=1600000, monthly_revenue=720000,  employee_count=615, funding_raised=80000000,  burn_rate=560000),

        # Groww — strong growth
        Metrics(startup_id=startups[3].id, month=date(2024,1,1), monthly_users=3000000, monthly_revenue=1200000, employee_count=900, funding_raised=150000000, burn_rate=700000),
        Metrics(startup_id=startups[3].id, month=date(2024,2,1), monthly_users=3500000, monthly_revenue=1400000, employee_count=950, funding_raised=150000000, burn_rate=720000),
        Metrics(startup_id=startups[3].id, month=date(2024,3,1), monthly_users=4100000, monthly_revenue=1700000, employee_count=990, funding_raised=150000000, burn_rate=740000),

        # Meesho — struggling, low runway
        Metrics(startup_id=startups[4].id, month=date(2024,1,1), monthly_users=800000,  monthly_revenue=300000,  employee_count=400, funding_raised=3000000,   burn_rate=600000),
        Metrics(startup_id=startups[4].id, month=date(2024,2,1), monthly_users=780000,  monthly_revenue=270000,  employee_count=390, funding_raised=3000000,   burn_rate=650000),
        Metrics(startup_id=startups[4].id, month=date(2024,3,1), monthly_users=750000,  monthly_revenue=240000,  employee_count=375, funding_raised=3000000,   burn_rate=700000),
    ]
    db.add_all(metrics_data)
    db.commit()
    db.close()
    print("✅ Seed data inserted — 5 startups, 3 months each")


if __name__ == "__main__":
    seed()