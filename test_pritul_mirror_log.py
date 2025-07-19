"""
Tests for pritul_mirror_log module

This module contains basic tests to validate the Pritul Mirror Log data
structure and functionality.
"""

import os
import sys
import unittest

# Add parent directory to path to import pritul_mirror_log
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pritul_mirror_log import (
    pritul_mirror_data,
    get_interaction_summary,
    get_emotional_metrics,
    validate_data_structure
)

class TestPritulMirrorLog(unittest.TestCase):
    """Test cases for Pritul Mirror Log functionality."""

    def test_data_structure_validation(self):
        """Test that the data structure is valid."""
        self.assertTrue(validate_data_structure())

    def test_required_fields_exist(self):
        """Test that all required fields exist in the data structure."""
        required_fields = ["title", "date", "human_input", "ai_response", "summary"]
        for field in required_fields:
            self.assertIn(field, pritul_mirror_data)

    def test_interaction_summary(self):
        """Test the interaction summary function."""
        summary = get_interaction_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn("interaction_type", summary)
        self.assertIn("rarity_estimate", summary)
        self.assertIn("significance", summary)
        self.assertEqual(summary["interaction_type"], "Legacy-Class Emotional Mirror")

    def test_emotional_metrics(self):
        """Test the emotional metrics function."""
        metrics = get_emotional_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("human_emotional_force", metrics)
        self.assertIn("ai_emotional_output_score", metrics)
        self.assertIn("deviation_status", metrics)

        # Test that emotional scores are within expected range
        self.assertGreaterEqual(metrics["human_emotional_force"], 0)
        self.assertLessEqual(metrics["human_emotional_force"], 10)
        self.assertGreaterEqual(metrics["ai_emotional_output_score"], 0)
        self.assertLessEqual(metrics["ai_emotional_output_score"], 10)

    def test_data_integrity(self):
        """Test data integrity and expected values."""
        # Test human input structure
        human_input = pritul_mirror_data["human_input"]
        self.assertEqual(human_input["name"], "Affan Aziz Pritul")
        self.assertEqual(human_input["alias"], "P2L")
        self.assertIsInstance(human_input["themes"], list)
        self.assertIsInstance(human_input["key_lines"], list)

        # Test AI response structure
        ai_response = pritul_mirror_data["ai_response"]
        self.assertEqual(ai_response["model"], "GPT-4 Turbo")
        self.assertIsInstance(ai_response["changes"], list)
        self.assertIsInstance(ai_response["reflections"], list)

    def test_date_format(self):
        """Test that the date is in expected format."""
        date = pritul_mirror_data["date"]
        self.assertIsInstance(date, str)
        # Basic check that it contains expected date components
        self.assertIn("2025", date)
        self.assertIn("05", date)  # May
        self.assertIn("06", date)  # Day

if __name__ == "__main__":
    unittest.main()
