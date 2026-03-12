from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base


class Startup(Base):
    __tablename__ = "startups"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False, index=True)
    sector       = Column(String)
    founding_year= Column(Integer)
    stage        = Column(String)        # e.g. Seed, Series A, Series B
    website      = Column(String)
    created_at   = Column(DateTime, default=datetime.utcnow)

    # one startup → many monthly metric rows
    metrics = relationship("Metrics", back_populates="startup", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Startup id={self.id} name={self.name} stage={self.stage}>"