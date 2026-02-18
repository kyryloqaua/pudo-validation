# PUDO Validation Mini Project

This project simulates Pickup/Dropoff (PUDO) validation logic for an autonomous vehicle system.

---

## 🧪 Test Coverage & Validation Strategy

This project includes 10 unit tests that validate both geometric calculations and business logic for PUDO (Pickup/Drop-off) validation.

### 1️⃣ Distance Calculation Tests

#### ✅ `test_distance_same_location`
Verifies that the distance between identical GPS coordinates is effectively zero.  
Ensures baseline correctness of the distance function.

#### ✅ `test_distance_different_locations`
Validates that distance between San Francisco and Las Vegas falls within realistic bounds (~600–900 km).  
Confirms scale accuracy of the geographic calculation.

---

### 2️⃣ Parking Logic Tests

The `can_vehicle_park()` function enforces the following rules:

- Zone must be active
- Vehicle must be within proximity threshold (≤ 10 meters)
- Vehicle speed must be < 1.0 m/s
- Pickup zones require empty vehicles
- Dropoff zones require occupied vehicles

Each test isolates a specific rule to ensure deterministic validation.

---

#### ✅ `test_valid_parking`
Validates the “happy path” scenario where all conditions are satisfied:
- Active zone
- Vehicle within threshold
- Speed below limit
- Correct occupancy state

Expected result: Parking allowed.

---

#### ❌ `test_inactive_zone_blocks`
Ensures that inactive zones immediately block parking regardless of other conditions.

Expected result: Parking denied.

---

#### ❌ `test_speed_too_high_blocks`
Validates that vehicles moving at or above the threshold (≥ 1.0 m/s) cannot park.

Expected result: Parking denied.

---

#### ❌ `test_occupied_in_pickup_zone_blocks`
Ensures that occupied vehicles cannot use pickup-only zones.

Expected result: Parking denied.

---

#### 🔄 `test_dropoff_requires_occupied`
Validates dropoff zone logic:
- Empty vehicle → denied
- Occupied vehicle → allowed

Ensures proper enforcement of dropoff-specific rule.

---

#### ❌ `test_distance_too_far_blocks`
Validates that vehicles beyond the proximity threshold cannot park, even if other conditions are met.

Expected result: Parking denied.

---

#### ✅ `test_distance_within_threshold_allows_parking`
Ensures that vehicles within the proximity threshold are eligible to park when all other conditions are satisfied.

Expected result: Parking allowed.

---

### 🎯 Validation Philosophy

Each test isolates a single business rule to ensure:

- Deterministic failure behavior  
- Clear root cause identification  
- No overlapping condition interference  
- Balanced positive and negative scenarios  

This approach mirrors real-world AV validation strategy where individual constraints must be independently verified before integration-level testing.


## Features

- Distance calculation between GPS coordinates
- Parking validation logic based on:
  - Zone activation state
  - Proximity threshold
  - Speed threshold
  - Pickup/dropoff occupancy rules

## Running Tests

```bash
python -m unittest -v
