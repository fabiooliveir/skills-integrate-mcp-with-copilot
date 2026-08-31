import unittest

from fastapi.testclient import TestClient

from src.app import ACTIVITY_RULES, activities, app


class ActivityRulesTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        for activity in activities.values():
            activity["participants"] = []

        activities["Chess Club"]["participants"] = [
            f"student{i}@mergington.edu"
            for i in range(activities["Chess Club"]["max_participants"])
        ]

        activities["Programming Class"]["participants"] = [
            "limitstudent@mergington.edu"
        ]
        activities["Gym Class"]["participants"] = [
            "limitstudent@mergington.edu"
        ]

    def test_signup_rejects_when_activity_is_full(self):
        response = self.client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("already full", response.json()["detail"]) 

    def test_signup_rejects_when_student_exceeds_max_activities(self):
        response = self.client.post(
            "/activities/Art Club/signup",
            params={"email": "limitstudent@mergington.edu"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("maximum number of activities", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
