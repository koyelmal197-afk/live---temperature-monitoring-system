from database import query_latest

def check_alert(sensor_id: str):
    rows = query_latest(sensor_id, 1)
    if rows:
        temp = rows[0]["temperature"]
        if temp > 30:
            return f"⚠ High Temperature Alert: {temp} °C"
    return "✅ Temperature Normal"