from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Metrics(Base):
    __tablename__ = "metrics"

    id             = Column(Integer, primary_key=True, index=True)
    startup_id     = Column(Integer, ForeignKey("startups.id"), nullable=False)
    month          = Column(Date, nullable=False)       # e.g. 2024-03-01
    monthly_users  = Column(Integer, default=0)
    monthly_revenue= Column(Float,   default=0.0)
    employee_count = Column(Integer, default=1)
    funding_raised = Column(Float,   default=0.0)
    burn_rate      = Column(Float,   default=0.0)
    created_at     = Column(DateTime, default=datetime.utcnow)

    # back-reference to parent startup
    startup = relationship("Startup", back_populates="metrics")

    def __repr__(self):
        return f"<Metrics startup_id={self.startup_id} month={self.month}>"