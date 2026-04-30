import unittest

from facility import Facility
from triage import determine_care_level
from filters import (
    filter_by_category,
    filter_by_city,
    filter_by_walk_in,
    recommend_facilities
)


class TestHealthcareNavigator(unittest.TestCase):
    def setUp(self):
        row1 = {
            "id": "1",
            "name": "Sample ER Cambridge",
            "category": "ER",
            "city": "Cambridge",
            "address": "123 Main St",
            "phone": "617-000-0001",
            "walk_in": "no",
            "hours": "24/7",
            "cost_level": "3",
            "notes": "Emergency care",
            "latitude": "42.3736",
            "longitude": "-71.1097"
        }

        row2 = {
            "id": "2",
            "name": "Sample Urgent Care Boston",
            "category": "URGENT_CARE",
            "city": "Boston",
            "address": "20 Second St",
            "phone": "617-000-0200",
            "walk_in": "yes",
            "hours": "9am-7pm",
            "cost_level": "2",
            "notes": "Walk-in urgent care",
            "latitude": "42.3503",
            "longitude": "-71.0786"
        }

        row3 = {
            "id": "3",
            "name": "Sample Primary Care Cambridge",
            "category": "PRIMARY_CARE",
            "city": "Cambridge",
            "address": "30 Third St",
            "phone": "617-000-0300",
            "walk_in": "no",
            "hours": "Mon-Fri 9am-5pm",
            "cost_level": "1",
            "notes": "Routine care",
            "latitude": "42.3939",
            "longitude": "-71.1455"
        }

        row4 = {
            "id": "4",
            "name": "Sample Telehealth Remote",
            "category": "TELEHEALTH",
            "city": "Remote",
            "address": "Online",
            "phone": "800-000-0000",
            "walk_in": "yes",
            "hours": "24/7",
            "cost_level": "1",
            "notes": "Remote service",
            "latitude": "0",
            "longitude": "0"
        }

        self.facilities = [Facility(row1), Facility(row2), Facility(row3), Facility(row4)]

    def test_determine_care_level(self):
        self.assertEqual(determine_care_level(True, False, False), "ER")
        self.assertEqual(determine_care_level(False, True, False), "URGENT_CARE")
        self.assertEqual(determine_care_level(False, False, True), "PRIMARY_CARE")
        self.assertEqual(determine_care_level(False, False, False), "TELEHEALTH")

    def test_filter_by_category(self):
        matches = filter_by_category(self.facilities, "ER")
        self.assertEqual(len(matches), 1)

    def test_filter_by_city_case_insensitive(self):
        matches = filter_by_city(self.facilities, "cambridge")
        self.assertEqual(len(matches), 3)

    def test_filter_by_walk_in(self):
        matches = filter_by_walk_in(self.facilities, True)
        self.assertEqual(len(matches), 2)

    def test_recommend_exact(self):
        match_type, ranked = recommend_facilities(
            self.facilities, "URGENT_CARE", "Boston", True
        )
        self.assertEqual(match_type, "exact")
        self.assertEqual(ranked[0][1].name, "Sample Urgent Care Boston")

    def test_recommend_fallback(self):
        match_type, ranked = recommend_facilities(
            self.facilities, "ER", "Boston", True
        )
        self.assertEqual(match_type, "fallback")
        self.assertEqual(ranked[0][1].name, "Sample ER Cambridge")


if __name__ == "__main__":
    unittest.main()