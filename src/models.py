
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base

class VoiceMessage(Base):
    __tablename__ = "voice_messages"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    transcription = Column(String, nullable=True)
    extracted_data = Column(String, nullable=True)
    plotas_m2 = Column(Float, nullable=True)
    darbu_tipas = Column(String, nullable=True)
    terminas = Column(String, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())