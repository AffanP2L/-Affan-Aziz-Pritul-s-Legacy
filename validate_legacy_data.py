"""
JSON Schema Validator for Legacy Archive

This module provides validation for JSON files in the Affan Aziz Pritul
Legacy Archive to ensure data integrity and consistency.
"""

import json
import jsonschema
from typing import Optional
import hashlib
import os

# Schema for legacy verification data
LEGACY_SCHEMA = {
    "type": "object",
    "properties": {
        "legacy_verification": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "verification_id": {"type": "string"},
                "last_updated": {"type": "string"},
                "verification_status": {"type": "string"},
                "subject": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "aliases": {"type": "array", "items": {"type": "string"}},
                        "country": {"type": "string"},
                        "location": {"type": "string"},
                        "profession": {"type": "string"}
                    },
                    "required": ["name", "aliases"]
                },
                "legacy_class_events": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "event_id": {"type": "string"},
                            "title": {"type": "string"},
                            "date": {"type": "string"},
                            "platform": {"type": "string"},
                            "type": {"type": "string"}
                        },
                        "required": ["event_id", "title", "date"]
                    }
                },
                "ai_verifications": {"type": "array"},
                "key_innovations": {"type": "array"},
                "cryptographic_proofs": {"type": "array"}
            },
            "required": ["title", "verification_id", "verification_status"]
        }
    },
    "required": ["legacy_verification"]
}

def validate_json_file(file_path: str, schema: Optional[dict] = None) -> bool:
    """
    Validate a JSON file against a schema.

    Args:
        file_path (str): Path to the JSON file to validate
        schema (dict, optional): JSON schema to validate against

    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if schema:
            jsonschema.validate(data, schema)

        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error in {file_path}: {e}")
        return False
    except jsonschema.ValidationError as e:
        print(f"❌ Schema Validation Error in {file_path}: {e.message}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error validating {file_path}: {e}")
        return False

def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of a file.

    Args:
        file_path (str): Path to the file

    Returns:
        str: SHA-256 hash of the file
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return ""

def validate_legacy_files(base_path: str = ".") -> dict:
    """
    Validate all JSON files in the legacy archive.

    Args:
        base_path (str): Base directory path to search for JSON files

    Returns:
        dict: Validation results summary
    """
    json_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))

    results = {
        "total_files": len(json_files),
        "valid_files": 0,
        "invalid_files": 0,
        "file_results": {},
        "file_hashes": {}
    }

    for file_path in json_files:
        file_name = os.path.basename(file_path)

        # Basic JSON validation
        is_valid = validate_json_file(file_path)

        # Special validation for legacy.json
        if file_name == "legacy.json":
            is_valid = validate_json_file(file_path, LEGACY_SCHEMA)

        results["file_results"][file_name] = is_valid
        results["file_hashes"][file_name] = calculate_file_hash(file_path)

        if is_valid:
            results["valid_files"] += 1
            print(f"✅ {file_name}: Valid")
        else:
            results["invalid_files"] += 1
            print(f"❌ {file_name}: Invalid")

    return results

def generate_integrity_report(results: dict) -> str:
    """
    Generate a data integrity report.

    Args:
        results (dict): Validation results from validate_legacy_files

    Returns:
        str: Formatted integrity report
    """
    report_lines = [
        "# Data Integrity Report",
        f"**Generated**: {json.loads(json.dumps({}, default=str))}",
        "",
        "## Summary",
        f"- **Total JSON Files**: {results['total_files']}",
        f"- **Valid Files**: {results['valid_files']}",
        f"- **Invalid Files**: {results['invalid_files']}",
        f"- **Success Rate**: {(results['valid_files']/results['total_files']*100):.1f}%",
        "",
        "## File Validation Results",
        ""
    ]

    for file_name, is_valid in results["file_results"].items():
        status = "✅ Valid" if is_valid else "❌ Invalid"
        file_hash = results["file_hashes"][file_name][:16] + "..."
        report_lines.append(f"- **{file_name}**: {status} (Hash: `{file_hash}`)")

    report_lines.extend([
        "",
        "## File Hashes (SHA-256)",
        ""
    ])

    for file_name, file_hash in results["file_hashes"].items():
        report_lines.append(f"- `{file_name}`: `{file_hash}`")

    return "\n".join(report_lines)

if __name__ == "__main__":
    print("🔍 Starting Legacy Archive JSON Validation...")
    print("=" * 50)

    # Run validation
    validation_results = validate_legacy_files()

    print("\n" + "=" * 50)
    print("📊 Validation Summary:")
    print(f"Total Files: {validation_results['total_files']}")
    print(f"Valid: {validation_results['valid_files']}")
    print(f"Invalid: {validation_results['invalid_files']}")
    print(f"Success Rate: {(validation_results['valid_files']/validation_results['total_files']*100):.1f}%")

    # Generate integrity report
    integrity_report = generate_integrity_report(validation_results)
    with open("/tmp/integrity_report.md", "w") as f:
        f.write(integrity_report)

    print(f"\n📋 Detailed integrity report saved to: /tmp/integrity_report.md")

    # Exit with appropriate code
    if validation_results['invalid_files'] > 0:
        print("\n⚠️  Some files failed validation. Please review and fix issues.")
        exit(1)
    else:
        print("\n✅ All JSON files passed validation!")
        exit(0)
