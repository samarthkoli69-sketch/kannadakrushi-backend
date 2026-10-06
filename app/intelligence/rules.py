def generate_field_alerts(reading):
    alerts = []

    if reading.soil_moisture is not None:
        if reading.soil_moisture < 30:
            alerts.append({
                "alert_type": "IRRIGATION",
                "severity": "high",
                "title": "Low soil moisture",
                "message": "Soil moisture is low. Check the field and irrigation requirement."
            })

    if reading.water_level is not None:
        if reading.water_level < 20:
            alerts.append({
                "alert_type": "WATER",
                "severity": "high",
                "title": "Low water level",
                "message": "Available water level is low. Check the water source."
            })

    if reading.soil_ph is not None:
        if reading.soil_ph < 5.5 or reading.soil_ph > 8.0:
            alerts.append({
                "alert_type": "SOIL_PH",
                "severity": "medium",
                "title": "Soil pH needs attention",
                "message": "The measured soil pH is outside the basic monitoring range."
            })

    return alerts