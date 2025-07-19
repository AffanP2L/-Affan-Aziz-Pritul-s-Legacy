"""
Tests for validate_legacy_data module

This module contains tests for the JSON validation and integrity checking
functionality.
"""

import unittest
import os
import json
import tempfile
import shutil

from validate_legacy_data import (
    validate_json_file,
    calculate_file_hash,
    validate_legacy_files,
    generate_integrity_report,
    LEGACY_SCHEMA
)

class TestValidateLegacyData(unittest.TestCase):
    """Test cases for legacy data validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.valid_json = {"test": "data", "number": 42, "array": [1, 2, 3]}
        self.invalid_json_content = '{"invalid": json content}'

        # Create test JSON files
        self.valid_json_file = os.path.join(self.test_dir, "valid.json")
        with open(self.valid_json_file, 'w') as f:
            json.dump(self.valid_json, f)

        self.invalid_json_file = os.path.join(self.test_dir, "invalid.json")
        with open(self.invalid_json_file, 'w') as f:
            f.write(self.invalid_json_content)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_validate_valid_json_file(self):
        """Test validation of a valid JSON file."""
        result = validate_json_file(self.valid_json_file)
        self.assertTrue(result)

    def test_validate_invalid_json_file(self):
        """Test validation of an invalid JSON file."""
        result = validate_json_file(self.invalid_json_file)
        self.assertFalse(result)

    def test_validate_nonexistent_file(self):
        """Test validation of a non-existent file."""
        result = validate_json_file("nonexistent.json")
        self.assertFalse(result)

    def test_validate_with_schema(self):
        """Test validation with a JSON schema."""
        simple_schema = {
            "type": "object",
            "properties": {
                "test": {"type": "string"},
                "number": {"type": "number"}
            },
            "required": ["test"]
        }

        result = validate_json_file(self.valid_json_file, simple_schema)
        self.assertTrue(result)

    def test_calculate_file_hash(self):
        """Test file hash calculation."""
        file_hash = calculate_file_hash(self.valid_json_file)
        self.assertIsInstance(file_hash, str)
        self.assertEqual(len(file_hash), 64)  # SHA-256 produces 64-character hex string

    def test_calculate_hash_nonexistent_file(self):
        """Test hash calculation for non-existent file."""
        file_hash = calculate_file_hash("nonexistent.json")
        self.assertEqual(file_hash, "")

    def test_legacy_schema_structure(self):
        """Test that the legacy schema has required structure."""
        self.assertIn("type", LEGACY_SCHEMA)
        self.assertIn("properties", LEGACY_SCHEMA)
        self.assertIn("legacy_verification", LEGACY_SCHEMA["properties"])

    def test_validate_legacy_files_structure(self):
        """Test the structure of validate_legacy_files return value."""
        # Create a temporary directory with JSON files
        test_dir = tempfile.mkdtemp()
        try:
            test_file = os.path.join(test_dir, "test.json")
            with open(test_file, 'w') as f:
                json.dump({"test": "data"}, f)

            results = validate_legacy_files(test_dir)

            # Check result structure
            self.assertIn("total_files", results)
            self.assertIn("valid_files", results)
            self.assertIn("invalid_files", results)
            self.assertIn("file_results", results)
            self.assertIn("file_hashes", results)

            # Check data types
            self.assertIsInstance(results["total_files"], int)
            self.assertIsInstance(results["valid_files"], int)
            self.assertIsInstance(results["invalid_files"], int)
            self.assertIsInstance(results["file_results"], dict)
            self.assertIsInstance(results["file_hashes"], dict)

        finally:
            shutil.rmtree(test_dir)

    def test_generate_integrity_report(self):
        """Test integrity report generation."""
        mock_results = {
            "total_files": 2,
            "valid_files": 1,
            "invalid_files": 1,
            "file_results": {
                "valid.json": True,
                "invalid.json": False
            },
            "file_hashes": {
                "valid.json": "abc123def456",
                "invalid.json": "def456ghi789"
            }
        }

        report = generate_integrity_report(mock_results)

        self.assertIsInstance(report, str)
        self.assertIn("Data Integrity Report", report)
        self.assertIn("Total JSON Files", report)
        self.assertIn("valid.json", report)
        self.assertIn("invalid.json", report)
        self.assertIn("50.0%", report)  # Success rate

    def test_file_hash_consistency(self):
        """Test that file hash calculation is consistent."""
        hash1 = calculate_file_hash(self.valid_json_file)
        hash2 = calculate_file_hash(self.valid_json_file)
        self.assertEqual(hash1, hash2)

    def test_validation_with_empty_directory(self):
        """Test validation with an empty directory."""
        empty_dir = tempfile.mkdtemp()
        try:
            results = validate_legacy_files(empty_dir)
            self.assertEqual(results["total_files"], 0)
            self.assertEqual(results["valid_files"], 0)
            self.assertEqual(results["invalid_files"], 0)
        finally:
            shutil.rmtree(empty_dir)

if __name__ == "__main__":
    unittest.main()
