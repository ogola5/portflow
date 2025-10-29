# app/api/adapters.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.core.database import db
from app.services.parse_and_normalize import normalize_json_payload, parse_csv_bytes, normalize_from_ocr
from app.services.entity_resolution import resolve_and_link
from app.services.ocr_service import ocr_extract_text
import uuid, datetime, io, csv, json

router = APIRouter(tags=["Adapters"], prefix="/adapters")

# Generic webhook / API ingest (JSON)
@router.post("/webhook")
async def ingest_webhook(source: str = Form(...), payload: dict = Form(...)):
    """
    Example: send via form fields or JSON body. For JSON body prefer /adapters/webhook_json
    """
    raw_id = str(uuid.uuid4())
    raw_doc = {
        "_id": raw_id,
        "source": source,
        "format": "json",
        "raw_payload": payload,
        "received_at": datetime.datetime.utcnow().isoformat()
    }
    await db.raw_events.insert_one(raw_doc)

    canonical = normalize_json_payload(payload, source=source)
    entity_id, match = await resolve_and_link(canonical, raw_id)

    return {"status": "ok", "raw_id": raw_id, "entity_id": entity_id, "match": match}


@router.post("/webhook/json")
async def ingest_webhook_json(payload: dict, source: Optional[str] = "unknown"):
    raw_id = str(uuid.uuid4())
    raw_doc = {
        "_id": raw_id,
        "source": source,
        "format": "json",
        "raw_payload": payload,
        "received_at": datetime.datetime.utcnow().isoformat()
    }
    await db.raw_events.insert_one(raw_doc)

    canonical = normalize_json_payload(payload, source=source)
    entity_id, match = await resolve_and_link(canonical, raw_id)
    return {"status": "ok", "raw_id": raw_id, "entity_id": entity_id, "match": match}


# File upload (CSV manifest)
@router.post("/upload/csv")
async def ingest_csv(source: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    raw_id = str(uuid.uuid4())
    await db.raw_events.insert_one({
        "_id": raw_id,
        "source": source,
        "format": "csv",
        "filename": file.filename,
        "raw_payload": None,
        "file_ref": file.filename,
        "received_at": datetime.datetime.utcnow().isoformat()
    })

    # parse CSV into rows
    try:
        rows = parse_csv_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV parse error: {e}")

    results = []
    for row in rows:
        canonical = normalize_json_payload(row, source=source)
        entity_id, match = await resolve_and_link(canonical, raw_id)
        results.append({"entity_id": entity_id, "match": match, "row_key": row.get("container_id") or row.get("truck_id")})

    return {"status": "ok", "file": file.filename, "imported": len(results), "results": results}


# Image/document upload (photo of form / PDF page)
@router.post("/upload/image")
async def ingest_image(source: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    raw_id = str(uuid.uuid4())
    # save raw event metadata
    await db.raw_events.insert_one({
        "_id": raw_id,
        "source": source,
        "format": "image",
        "filename": file.filename,
        "file_ref": file.filename,
        "received_at": datetime.datetime.utcnow().isoformat()
    })

    # OCR extract text
    try:
        text = ocr_extract_text(content)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # attempt to parse key fields from OCR text
    canonical = normalize_from_ocr(text, source=source)
    entity_id, match = await resolve_and_link(canonical, raw_id)

    # persist extracted text for audit
    await db.ocr_results.insert_one({
        "raw_id": raw_id,
        "text": text,
        "filename": file.filename,
        "created_at": datetime.datetime.utcnow().isoformat()
    })

    return {"status": "ok", "raw_id": raw_id, "entity_id": entity_id, "match": match}
