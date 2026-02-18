from .models import PudoZone, Vehicle

SAMPLE_ZONES = [
    PudoZone("zone_001", "sf_mission_bay", 37.7749, -122.4194, 3, True,  "both"),
    PudoZone("zone_002", "sf_soma",        37.7849, -122.4094, 2, True,  "pickup"),
    PudoZone("zone_003", "sf_financial",   37.7949, -122.3994, 4, False, "dropoff"),
    PudoZone("zone_004", "vegas_strip",    36.1699, -115.1398, 5, True,  "both"),
]

SAMPLE_VEHICLES = [
    Vehicle("vh001", 37.7749, -122.4194, 0.5, False),
    Vehicle("vh002", 37.7849, -122.4094, 5.0, True),
    Vehicle("vh003", 36.1699, -115.1398, 0.3, False),
    Vehicle("vh004", 36.1699, -115.1398, 0.3, True)
]
