import math
from .models import Vehicle, PudoZone

MAX_DISTANCE_M = 10.0

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat_diff_m = (lat2 - lat1) * 111_000
    lon_diff_m = (lon2 - lon1) * 111_000 * math.cos(math.radians(lat1))
    return math.sqrt(lat_diff_m**2 + lon_diff_m**2)

def can_vehicle_park(vehicle: Vehicle, zone: PudoZone) -> bool:
    if not zone.is_active:
        return False

    distance = calculate_distance(vehicle.latitude, vehicle.longitude, zone.latitude, zone.longitude)
    if distance > MAX_DISTANCE_M:
        return False

    if vehicle.speed_mps >= 1.0:
        return False

    if zone.zone_type == "pickup" and vehicle.is_occupied:
        return False

    if zone.zone_type == "dropoff" and not vehicle.is_occupied:
        return False

    return True
