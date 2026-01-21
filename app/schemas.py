from pydantic import BaseModel
from typing import Optional, Dict


class OCRBlock(BaseModel):
    raw_text: str
    confidence: float


class EntityBlock(BaseModel):
    entities: Dict[str, Optional[str]]
    entities_confidence: float


class NormalizationBlock(BaseModel):
    normalized: Optional[Dict[str, str]]
    normalization_confidence: float


class AppointmentBlock(BaseModel):
    department: str
    date: str
    time: str
    tz: str


class FullResponse(BaseModel):
    ocr: Optional[OCRBlock] = None
    entity_extraction: Optional[EntityBlock] = None
    normalization: Optional[NormalizationBlock] = None
    appointment: Optional[AppointmentBlock] = None
    status: str
    message: Optional[str] = None
