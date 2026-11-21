"""storage.py 독립 테스트: python -m unittest -v test_storage.py"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        path = Path(self.temp_dir.name) / "schedules.json"
        patcher = patch.object(storage, "DATA_FILE", path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.example = [{
            "id": 1, "title": "파이썬 과제", "type": "assignment",
            "due_date": "2026-12-01", "priority": "high", "completed": False
        }]

    def test_complete_existing_id(self):
        result = storage.mark_completed(self.example, 1)
        self.assertIs(result, self.example)
        self.assertTrue(result[0]["completed"])

    def test_missing_id(self):
        result = storage.mark_completed(self.example, 999)
        self.assertIs(result, self.example)
        self.assertFalse(result[0]["completed"])

    def test_save_and_load(self):
        self.assertIsNone(storage.save_schedules(self.example))
        self.assertEqual(storage.load_schedules(), self.example)
        self.assertIn("파이썬 과제", storage.DATA_FILE.read_text(encoding="utf-8"))

    def test_missing_file_returns_empty(self):
        self.assertEqual(storage.load_schedules(), [])

    def test_invalid_json_raises_without_overwriting(self):
        storage.DATA_FILE.write_text("broken {", encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.load_schedules()
        self.assertEqual(storage.DATA_FILE.read_text(encoding="utf-8"), "broken {")

    def test_wrong_top_level_type_raises(self):
        storage.DATA_FILE.write_text(json.dumps({"id": 1}), encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.load_schedules()


if __name__ == "__main__":
    unittest.main()
