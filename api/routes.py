from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from database.connection import get_db
from models.startup import Startup
from models.metrics import Metrics
from analytics.growth import calculate_growth_series
from analytics.runway import calculate_runway
from analytics.trends import build_metrics_df, add_growth_columns
from scoring.health_score import calculate_health_score
from scoring.momentum import calculate_momentum_from_series
from alerts.rules import run_all_alerts

router = APIRouter()


# ── Pydantic schemas (request body shapes) ─────────────────

class StartupCreate(BaseModel):
    name:          str
    sector:        str
    founding_year: int
    stage:         str
    website:       str = ""

class MetricsCreate(BaseModel):
    startup_id:      int
    month:           date
    monthly_users:   int   = 0
    monthly_revenue: float = 0.0
    employee_count:  int   = 1
    funding_raised:  float = 0.0
    burn_rate:       float = 0.0


# ── POST /startup ───────────────────────────────────────────

@router.post("/startup", status_code=201)
def create_startup(data: StartupCreate, db: Session = Depends(get_db)):
    """Register a new startup."""
    existing = db.query(Startup).filter(Startup.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Startup name already exists")

    startup = Startup(**data.model_dump())
    db.add(startup)
    db.commit()
    db.refresh(startup)
    return {"message": "Startup created", "id": startup.id, "name": startup.name}


# ── POST /metrics ───────────────────────────────────────────

@router.post("/metrics", status_code=201)
def add_metrics(data: MetricsCreate, db: Session = Depends(get_db)):
    """Submit monthly metrics for a startup."""
    startup = db.query(Startup).filter(Startup.id == data.startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    # prevent duplicate month entry
    duplicate = db.query(Metrics).filter(
        Metrics.startup_id == data.startup_id,
        Metrics.month == data.month
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Metrics for this month already exist")

    # validate inputs
    if data.monthly_revenue < 0 or data.monthly_users < 0 or data.burn_rate < 0:
        raise HTTPException(status_code=422, detail="Metric values cannot be negative")

    metric = Metrics(**data.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return {"message": "Metrics added", "id": metric.id, "month": str(metric.month)}


# ── GET /startup/{id} ───────────────────────────────────────

@router.get("/startup/{startup_id}")
def get_startup(startup_id: int, db: Session = Depends(get_db)):
    """Return startup info, all metrics, health score, momentum and alerts."""
    startup = db.query(Startup).filter(Startup.id == startup_id).first()
    if not startup:
        raise HTTPException(status_code=404, detail="Startup not found")

    metrics_rows = (
        db.query(Metrics)
        .filter(Metrics.startup_id == startup_id)
        .order_by(Metrics.month)
        .all()
    )

    metrics_list = [
        {
            "month":           str(m.month),
            "monthly_users":   m.monthly_users,
            "monthly_revenue": m.monthly_revenue,
            "employee_count":  m.employee_count,
            "funding_raised":  m.funding_raised,
            "burn_rate":       m.burn_rate,
        }
        for m in metrics_rows
    ]

    # need at least 2 months for analysis
    if len(metrics_list) < 2:
        return {
            "startup": {"id": startup.id, "name": startup.name,
                        "sector": startup.sector, "stage": startup.stage},
            "metrics": metrics_list,
            "analysis": "Need at least 2 months of data for analysis"
        }

    df = build_metrics_df(metrics_list)
    df = add_growth_columns(df)

    latest       = df.iloc[-1]
    prev         = df.iloc[-2]
    runway       = calculate_runway(latest["funding_raised"], latest["burn_rate"])
    health       = calculate_health_score(
                       latest["revenue_growth"],
                       latest["user_growth"],
                       latest["employee_growth"],
                       runway)
    momentum     = calculate_momentum_from_series(df["revenue_growth"].tolist())
    alerts       = run_all_alerts(
                       runway,
                       latest["monthly_revenue"], prev["monthly_revenue"],
                       latest["burn_rate"],        prev["burn_rate"])

    return {
        "startup": {
            "id":      startup.id,
            "name":    startup.name,
            "sector":  startup.sector,
            "stage":   startup.stage,
            "website": startup.website,
        },
        "metrics": metrics_list,
        "analysis": {
            "health_score":    health["score"],
            "grade":           health["grade"],
            "breakdown":       health["breakdown"],
            "momentum":        momentum,
            "runway_months":   runway,
            "alerts":          alerts,
        }
    }


# ── GET /leaderboard ────────────────────────────────────────

@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Return all startups ranked by health score (highest first)."""
    startups = db.query(Startup).all()
    rankings = []

    for startup in startups:
        metrics_rows = (
            db.query(Metrics)
            .filter(Metrics.startup_id == startup.id)
            .order_by(Metrics.month)
            .all()
        )

        if len(metrics_rows) < 2:
            rankings.append({
                "rank":         None,
                "id":           startup.id,
                "name":         startup.name,
                "sector":       startup.sector,
                "stage":        startup.stage,
                "health_score": None,
                "grade":        "N/A",
                "note":         "Insufficient data"
            })
            continue

        metrics_list = [
            {
                "month":           str(m.month),
                "monthly_users":   m.monthly_users,
                "monthly_revenue": m.monthly_revenue,
                "employee_count":  m.employee_count,
                "funding_raised":  m.funding_raised,
                "burn_rate":       m.burn_rate,
            }
            for m in metrics_rows
        ]

        df      = build_metrics_df(metrics_list)
        df      = add_growth_columns(df)
        latest  = df.iloc[-1]
        runway  = calculate_runway(latest["funding_raised"], latest["burn_rate"])
        health  = calculate_health_score(
                      latest["revenue_growth"],
                      latest["user_growth"],
                      latest["employee_growth"],
                      runway)

        rankings.append({
            "rank":         None,
            "id":           startup.id,
            "name":         startup.name,
            "sector":       startup.sector,
            "stage":        startup.stage,
            "health_score": health["score"],
            "grade":        health["grade"],
        })

    # sort by score descending, None scores go to bottom
    rankings.sort(key=lambda x: x["health_score"] or -1, reverse=True)
    for i, r in enumerate(rankings):
        r["rank"] = i + 1

    return {"leaderboard": rankings, "total": len(rankings)}