import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timezone

from database import db, create_document, get_documents
from schemas import Vessel, Mission, CrewLog, Telemetry

app = FastAPI(title="Oceanographic Research Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Oceanographic Dashboard Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# --- Oceanographic endpoints ---

@app.post("/api/vessels", response_model=dict)
def create_vessel(v: Vessel):
    try:
        inserted_id = create_document("vessel", v)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vessels", response_model=List[dict])
def list_vessels(limit: Optional[int] = 50):
    try:
        docs = get_documents("vessel", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/missions", response_model=dict)
def create_mission(m: Mission):
    try:
        inserted_id = create_document("mission", m)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/missions", response_model=List[dict])
def list_missions(limit: Optional[int] = 50):
    try:
        docs = get_documents("mission", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/logs", response_model=dict)
def create_log(log: CrewLog):
    try:
        inserted_id = create_document("crewlog", log)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/logs", response_model=List[dict])
def list_logs(limit: Optional[int] = 100):
    try:
        docs = get_documents("crewlog", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/telemetry", response_model=dict)
def ingest_telemetry(t: Telemetry):
    try:
        inserted_id = create_document("telemetry", t)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/telemetry", response_model=List[dict])
def get_telemetry(limit: Optional[int] = 200):
    try:
        docs = get_documents("telemetry", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Simple mocked weather endpoint (could be replaced with real API call)
class WeatherQuery(BaseModel):
    lat: float
    lng: float


@app.post("/api/weather")
def get_weather(q: WeatherQuery):
    # Placeholder deterministic weather data based on lat/lng buckets
    try:
        sea_state = ["Calm", "Slight", "Moderate", "Rough"]
        idx = int(((abs(q.lat) + abs(q.lng)) % 4))
        return {
            "summary": f"{sea_state[idx]} seas",
            "wind_kts": 8 + idx * 5,
            "visibility_km": 20 - idx * 3,
            "wave_m": round(0.5 + idx * 0.7, 1),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
