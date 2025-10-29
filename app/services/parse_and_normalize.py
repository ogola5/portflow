# app/services/parse_and_normalize.py
from typing import Dict, Any, List
import csv, io, re, datetime

# Basic normalizer: map known source fields into canonical schema
def normalize_json_payload(payload: Dict[str, Any], source: str = "unknown") -> Dict[str, Any]:
    """
    Output canonical dict with keys:
      - entity_type: 'container'|'truck'|'unknown'
      - container_no, truck_id, kra_ref, event_type, timestamp, attributes
    """
    out = {"source": source, "attributes": {}, "timestamp": None, "entity_type": "unknown"}

    # heuristics for container id (ISO 6346 format loosely)
    def find_container(obj):
        for k,v in obj.items():
            try:
                if isinstance(v, str) and re.match(r'^[A-Z]{4}\d{7}$', v):
                    return v
            except Exception:
                continue
        return None

    # direct known fields
    if "container_id" in payload:
        out["container_no"] = payload.get("container_id")
        out["entity_type"] = "container"
    elif "container_no" in payload:
        out["container_no"] = payload.get("container_no")
        out["entity_type"] = "container"
    elif "truck_id" in payload:
        out["truck_id"] = payload.get("truck_id")
        out["entity_type"] = "truck"
    elif "plate" in payload:
        out["truck_id"] = payload.get("plate")
        out["entity_type"] = "truck"
    else:
        # attempt find container id in any string fields
        cont = find_container(payload)
        if cont:
            out["container_no"] = cont
            out["entity_type"] = "container"

    # KRA reference
    if "kra_ref" in payload:
        out["kra_ref"] = payload.get("kra_ref")

    # event and timestamp
    out["event_type"] = payload.get("event_type") or payload.get("status") or "unknown"
    ts = payload.get("timestamp") or payload.get("ts") or payload.get("time")
    if ts:
        try:
            out["timestamp"] = ts
        except Exception:
            out["timestamp"] = str(datetime.datetime.utcnow().isoformat())
    else:
        out["timestamp"] = str(datetime.datetime.utcnow().isoformat())

    # attributes: copy everything else
    for k,v in payload.items():
        if k not in ["container_id","container_no","truck_id","plate","kra_ref","event_type","status","timestamp","ts","time"]:
            out["attributes"][k] = v

    return out

def parse_csv_bytes(content: bytes) -> List[Dict[str, str]]:
    s = content.decode('utf-8', errors='ignore')
    reader = csv.DictReader(io.StringIO(s))
    return [dict(r) for r in reader]

# naive OCR text -> canonical extraction (very source-dependent)
def normalize_from_ocr(text: str, source: str = "ocr") -> Dict[str, any]:
    out = {"source": source, "attributes": {}, "timestamp": None, "entity_type": "unknown"}
    # container pattern
    m = re.search(r'([A-Z]{4}\d{7})', text)
    if m:
        out["container_no"] = m.group(1)
        out["entity_type"] = "container"
    # KRA ref pattern (example: KRA-12345)
    m2 = re.search(r'KRA[-\s]?(\d{3,10})', text, re.IGNORECASE)
    if m2:
        out["kra_ref"] = m2.group(0)
    # event keywords
    if "release" in text.lower() or "cleared" in text.lower():
        out["event_type"] = "cleared"
    # timestamp: naive search for ISO-like
    m3 = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', text)
    if m3:
        out["timestamp"] = m3.group(1)
    else:
        out["timestamp"] = str(datetime.datetime.utcnow().isoformat())

    out["attributes"]["ocr_snippet"] = text[:200]
    return out
