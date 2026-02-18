from dataclasses import dataclass

@dataclass
class PudoZone:
    zone_id: str
    zone_name: str
    latitude: float
    longitude: float
    capacity: int
    is_active: bool
    zone_type: str  # "pickup", "dropoff", "both"

@dataclass
class Vehicle:
    vehicle_id: str
    latitude: float
    longitude: float
    speed_mps: float
    is_occupied: bool
