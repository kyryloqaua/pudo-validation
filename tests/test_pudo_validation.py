import unittest
from pudo.logic import calculate_distance, can_vehicle_park
from pudo.fixtures import SAMPLE_ZONES, SAMPLE_VEHICLES
from pudo.models import Vehicle, PudoZone


class TestPudoValidation(unittest.TestCase):

    def setUp(self):
        self.zone_active = SAMPLE_ZONES[0]    # active, both
        self.zone_pickup = SAMPLE_ZONES[1]    # active, pickup
        self.zone_inactive = SAMPLE_ZONES[2]  # inactive (blocks everything)

        self.vehicle_slow_empty = SAMPLE_VEHICLES[0]     # should be at zone_active
        self.vehicle_fast_occupied = SAMPLE_VEHICLES[1]  # fast, occupied

        # Create a dropoff-only ACTIVE zone at the same coords as zone_active
        # so distance doesn't interfere and we isolate the dropoff rule.
        self.dropoff_zone = PudoZone(
            zone_id="zone_dropoff_only",
            zone_name="sf_dropoff_only",
            latitude=self.zone_active.latitude,
            longitude=self.zone_active.longitude,
            capacity=2,
            is_active=True,
            zone_type="dropoff"
        )

        # Create a slow occupied vehicle at the dropoff zone (again: isolate dropoff rule)
        self.occupied_vehicle = Vehicle(
            "vh_occ",
            self.dropoff_zone.latitude,
            self.dropoff_zone.longitude,
            0.2,
            True
        )

    def test_distance_same_location(self):
        distance = calculate_distance(37.7749, -122.4194, 37.7749, -122.4194)
        self.assertLess(distance, 0.1)

    def test_distance_different_locations(self):
        distance = calculate_distance(37.7749, -122.4194, 36.1699, -115.1398)
        self.assertGreater(distance, 600_000)
        self.assertLess(distance, 900_000)

    def test_valid_parking(self):
        # assumes vehicle_slow_empty is at/near zone_active in fixtures
        self.assertTrue(can_vehicle_park(self.vehicle_slow_empty, self.zone_active))

    def test_inactive_zone_blocks(self):
        self.assertFalse(can_vehicle_park(self.vehicle_slow_empty, self.zone_inactive))

    def test_speed_too_high_blocks(self):
        # isolate speed: put vehicle exactly at the zone
        fast_vehicle = Vehicle(
            "vh_fast",
            self.zone_active.latitude,
            self.zone_active.longitude,
            1.5,
            False
        )
        self.assertFalse(can_vehicle_park(fast_vehicle, self.zone_active))

    def test_occupied_in_pickup_zone_blocks(self):
        # isolate occupancy: slow occupied vehicle at pickup zone
        slow_occupied = Vehicle(
            "vh_occ_pickup",
            self.zone_pickup.latitude,
            self.zone_pickup.longitude,
            0.2,
            True
        )
        self.assertFalse(can_vehicle_park(slow_occupied, self.zone_pickup))

    def test_dropoff_requires_occupied(self):
        # empty vehicle should NOT park in dropoff-only zone
        empty_vehicle_at_dropoff = Vehicle(
            "vh_empty_dropoff",
            self.dropoff_zone.latitude,
            self.dropoff_zone.longitude,
            0.2,
            False
        )
        self.assertFalse(can_vehicle_park(empty_vehicle_at_dropoff, self.dropoff_zone))

        # occupied vehicle SHOULD park in dropoff-only zone
        self.assertTrue(can_vehicle_park(self.occupied_vehicle, self.dropoff_zone))

    def test_speed_below_threshold_allows_parking(self):
        slow_vehicle = Vehicle(
            "vh_slow",
            self.zone_active.latitude,
            self.zone_active.longitude,
            0.9,
            False
        )
        fast_vehicle = Vehicle(
            "vh_fast2",
            self.zone_active.latitude,
            self.zone_active.longitude,
            1.5,
            False
        )
        self.assertTrue(can_vehicle_park(slow_vehicle, self.zone_active))
        self.assertFalse(can_vehicle_park(fast_vehicle, self.zone_active))

    def test_distance_too_far_blocks(self):
        # ~1.4km from zone_active -> should fail distance rule
        far_vehicle = Vehicle("vh_far", 37.7849, -122.4094, 0.5, False)
        self.assertFalse(can_vehicle_park(far_vehicle, self.zone_active))

    def test_distance_within_threshold_allows_parking(self):
        # must be within 10m: simplest is exactly at the zone
        near_vehicle = Vehicle(
            "vh_near",
            self.zone_active.latitude,
            self.zone_active.longitude,
            0.5,
            False
        )
        self.assertTrue(can_vehicle_park(near_vehicle, self.zone_active))


if __name__ == "__main__":
    unittest.main(verbosity=2)
