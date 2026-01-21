from fastapi import FastAPI, UploadFile, File, Form
from app.ocr import extract_text
from app.entity_extractor import extract_entities
from app.normalizer import normalize_date_time
from app.guardrails import needs_clarification
from app.schemas import FullResponse

app = FastAPI(title="AI Appointment Scheduler")


@app.post("/parse-appointment", response_model=FullResponse)
async def parse_appointment(
    text: str = Form(None),
    image: UploadFile = File(None),
):
    image_bytes = await image.read() if image else None

    DEPARTMENT_MAP = {
    "dentist": "Dentistry",
    "doctor": "General Medicine",
    "cardiology": "Cardiology",
    "orthopedic": "Orthopedics",
    }


    # STEP 1: OCR / TEXT EXTRACTION
    raw_text, ocr_conf = extract_text(text, image_bytes)

    if not raw_text:
        return FullResponse(
            status="needs_clarification",
            message="Unable to extract text",
        )

    ocr_block = {
        "raw_text": raw_text,
        "confidence": ocr_conf,
    }

    # STEP 2: ENTITY EXTRACTION
    entities, entity_conf = extract_entities(raw_text)

    entity_block = {
        "entities": entities,
        "entities_confidence": entity_conf,
    }

    if needs_clarification(entities):
        return FullResponse(
            ocr=ocr_block,
            entity_extraction=entity_block,
            status="needs_clarification",
            message="Ambiguous date/time or department",
        )

    # STEP 3: NORMALIZATION
    normalized, norm_conf = normalize_date_time(
        entities["date_phrase"], entities["time_phrase"]
    )

    normalization_block = {
        "normalized": normalized,
        "normalization_confidence": norm_conf,
    }

    if not normalized:
        return FullResponse(
            ocr=ocr_block,
            entity_extraction=entity_block,
            normalization=normalization_block,
            status="needs_clarification",
            message="Unable to normalize date/time",
        )

    # STEP 4: FINAL APPOINTMENT
    appointment = {
        "department": DEPARTMENT_MAP.get(
         entities["department"], entities["department"]
    ),

        "date": normalized["date"],
        "time": normalized["time"],
        "tz": normalized["tz"],
    }

    return FullResponse(
        ocr=ocr_block,
        entity_extraction=entity_block,
        normalization=normalization_block,
        appointment=appointment,
        status="ok",
    )
