from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine

# ============================================================
# MODELS
# ============================================================

from app.models import (
    User,
    Farm,
    Field,
    Crop,
    Sensor,
    SensorReading,
    DiseaseScan,
    Alert,
    Task,
    Recommendation,
)

from app.models.livestock import Livestock
from app.models.livestock_health_record import LivestockHealthRecord
from app.models.livestock_vaccination import LivestockVaccination


# ============================================================
# ROUTES
# ============================================================

from app.api.routes import (
    auth,
    health,
    users,
    farms,
    fields,
    crops,
    iot,
    plant_health,
    alerts,
    recommendations,
    weather,
    satellite,
    ai,
    livestock,
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="KannadaKrishi API",
    description="Smart Agriculture Platform Backend",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# AUTHENTICATION
# ============================================================

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# ============================================================
# HEALTH
# ============================================================

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)


# ============================================================
# USERS
# ============================================================

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)


# ============================================================
# FARMS
# ============================================================

app.include_router(
    farms.router,
    prefix="/api/v1/farms",
    tags=["Farms"],
)


# ============================================================
# FIELDS
# ============================================================

app.include_router(
    fields.router,
    prefix="/api/v1/fields",
    tags=["Fields"],
)


# ============================================================
# CROPS
# ============================================================

app.include_router(
    crops.router,
    prefix="/api/v1/crops",
    tags=["Crops"],
)


# ============================================================
# LIVESTOCK
# ============================================================

app.include_router(
    livestock.router,
    prefix="/api/v1/livestock",
    tags=["Livestock"],
)


# ============================================================
# IOT
# ============================================================

app.include_router(
    iot.router,
    prefix="/api/v1/iot",
    tags=["IoT"],
)


# ============================================================
# PLANT HEALTH
# ============================================================

app.include_router(
    plant_health.router,
    prefix="/api/v1/plant-health",
    tags=["Plant Health"],
)


# ============================================================
# ALERTS
# ============================================================

app.include_router(
    alerts.router,
    prefix="/api/v1/alerts",
    tags=["Alerts"],
)


# ============================================================
# RECOMMENDATIONS
# ============================================================

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["Recommendations"],
)


# ============================================================
# WEATHER
# ============================================================

app.include_router(
    weather.router,
    prefix="/api/v1/weather",
    tags=["Weather"],
)


# ============================================================
# SATELLITE
# ============================================================

app.include_router(
    satellite.router,
    prefix="/api/v1/satellite",
    tags=["Satellite"],
)


# ============================================================
# AI AGENT
# ============================================================

app.include_router(
    ai.router,
    prefix="/api/v1/ai",
    tags=["AI Agent"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Welcome to KannadaKrishi API",
        "version": "1.0.0",
        "status": "running",
    }