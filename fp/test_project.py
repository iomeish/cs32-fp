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
            "name": "Sample ER Boston",
            "category": "ER",
            "city": "Boston",
            "address": "55 Fruit St Boston MA",
            "phone": "617-726-2000",
            "walk_in": "no",
            "hours": "24/7",
            "cost_level": "3",
            "notes": "Emergency care",
            "latitude": "42.3628",
            "longitude": "-71.0690"
        }

        row2 = {
            "id": "2",
            "name": "Sample ER Cambridge",
            "category": "ER",
            "city": "Cambridge",
            "address": "1493 Cambridge St Cambridge MA",
            "phone": "617-665-1000",
            "walk_in": "no",
            "hours": "24/7",
            "cost_level": "3",
            "notes": "Emergency care",
            "latitude": "42.3736",
            "longitude": "-71.1097"
        }

        row3 = {
            "id": "3",
            "name": "Sample Urgent Care Boston",
            "category": "URGENT_CARE",
            "city": "Boston",
            "address": "137 Stuart St Boston MA",
            "phone": "617-393-5059",
            "walk_in": "yes",
            "hours": "Daily 9am-8:30pm",
            "cost_level": "2",
            "notes": "Walk-in urgent care",
            "latitude": "42.3513",
            "longitude": "-71.0670"
        }

        row4 = {
            "id": "4",
            "name": "Sample Urgent Care Cambridge",
            "category": "URGENT_CARE",
            "city": "Cambridge",
            "address": "215 Alewife Brook Pkwy Cambridge MA",
            "phone": "866-389-2727",
            "walk_in": "yes",
            "hours": "See website for current hours",
            "cost_level": "1",
            "notes": "Walk-in urgent care",
            "latitude": "42.3959",
            "longitude": "-71.1429"
        }

        row5 = {
            "id": "5",
            "name": "Sample Primary Care Cambridge",
            "category": "PRIMARY_CARE",
            "city": "Cambridge",
            "address": "119 Windsor St Cambridge MA",
            "phone": "617-665-3600",
            "walk_in": "no",
            "hours": "See website for current hours",
            "cost_level": "1",
            "notes": "Primary care",
            "latitude": "42.3647",
            "longitude": "-71.0966"
        }

        row6 = {
            "id": "6",
            "name": "Sample Telehealth Remote",
            "category": "TELEHEALTH",
            "city": "Remote",
            "address": "Online",
            "phone": "N/A",
            "walk_in": "yes",
            "hours": "24/7",
            "cost_level": "1",
            "notes": "Remote care",
            "latitude": "0",
            "longitude": "0"
        }

        self.facilities = [
            Facility(row1),
            Facility(row2),
            Facility(row3),
            Facility(row4),
            Facility(row5),
            Facility(row6)
        ]

    def test_determine_care_level(self):
        self.assertEqual(determine_care_level(True, False, False), "ER")
        self.assertEqual(determine_care_level(False, True, False), "URGENT_CARE")
        self.assertEqual(determine_care_level(False, False, True), "PRIMARY_CARE")
        self.assertEqual(determine_care_level(False, False, False), "TELEHEALTH")

    def test_filter_by_category(self):
        matches = filter_by_category(self.facilities, "ER")
        self.assertEqual(len(matches), 2)

    def test_filter_by_city_case_insensitive(self):
        matches = filter_by_city(self.facilities, "cambridge")
        self.assertEqual(len(matches), 4)

    def test_filter_by_walk_in(self):
        matches = filter_by_walk_in(self.facilities, True)
        self.assertEqual(len(matches), 3)

    def test_recommend_exact(self):
        user_location = (42.3601, -71.0589)

        match_type, ranked = recommend_facilities(
            self.facilities, "URGENT_CARE", "Boston", True, user_location
        )

        self.assertEqual(match_type, "exact")
        self.assertEqual(ranked[0][1].name, "Sample Urgent Care Boston")

    def test_recommend_fallback(self):
        user_location = (42.3601, -71.0589)

        match_type, ranked = recommend_facilities(
            self.facilities, "ER", "Boston", True, user_location
        )

        self.assertEqual(match_type, "fallback")
        self.assertEqual(ranked[0][1].name, "Sample ER Boston")

    def test_distance_ranking_prefers_nearer_facility(self):
        user_location = (42.3736, -71.1097)

        match_type, ranked = recommend_facilities(
            self.facilities, "URGENT_CARE", "", True, user_location
        )

        self.assertEqual(ranked[0][1].name, "Sample Urgent Care Cambridge")


if __name__ == "__main__":
    unittest.main()