"""
Database Schemas for Oceanographic Dashboard

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name (e.g., Vessel -> "vessel").
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Vessel(BaseModel):
    name: str = Field(..., description="Vessel name")
    imo: Optional[str] = Field(None, description="International Maritime Organization number")
    callsign: Optional[str] = Field(None, description="Radio callsign")
    lat: float = Field(..., ge=-90, le=90, description="Current latitude")
    lng: float = Field(..., ge=-180, le=180, description="Current longitude")
    heading: Optional[float] = Field(0, ge=0, le=360, description="Heading in degrees")
    speed: Optional[float] = Field(0, ge=0, description="Speed in knots")
    status: str = Field("active", description="active | docked | maintenance")


class Mission(BaseModel):
    vessel_id: Optional[str] = Field(None, description="Associated vessel id (string)")
    title: str = Field(..., description="Mission title")
    summary: Optional[str] = Field(None, description="Short summary")
    region: Optional[str] = Field(None, description="Oceanic region")
    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date (if completed)")
    status: str = Field("ongoing", description="ongoing | planned | complete")


class CrewLog(BaseModel):
    vessel_id: Optional[str] = Field(None, description="Associated vessel id (string)")
    author: str = Field(..., description="Crew member name")
    role: Optional[str] = Field(None, description="Crew role")
    message: str = Field(..., description="Log entry")
    severity: Optional[str] = Field("info", description="info | notice | warning | critical")


class Telemetry(BaseModel):
    vessel_id: Optional[str] = Field(None, description="Associated vessel id (string)")
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    depth: Optional[float] = Field(None, ge=0, description="Depth in meters")
    temperature: Optional[float] = Field(None, description="Sea temperature in °C")
    salinity: Optional[float] = Field(None, description="Salinity PSU")


# Example schemas kept for reference (not used by the UI)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True


class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
