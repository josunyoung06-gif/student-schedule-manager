"""storage.py 독립 검증: py -3 -m unittest -v test_storage.py"""

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
            "due_date": "2026-12-01", "priority": "high", "completed": False,
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

    def test_multiple_schedules_change_only_target(self):
        two = [dict(self.example[0]), dict(self.example[0], id=9, title="시험")]
        storage.mark_completed(two, 9)
        self.assertFalse(two[0]["completed"])
        self.assertTrue(two[1]["completed"])

    def test_already_complete_remains_true(self):
        self.example[0]["completed"] = True
        storage.mark_completed(self.example, 1)
        self.assertTrue(self.example[0]["completed"])

    def test_empty_list_round_trip(self):
        storage.save_schedules([])
        self.assertEqual(storage.load_schedules(), [])

    def test_invalid_item_rejected(self):
        storage.DATA_FILE.write_text("[42]", encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.load_schedules()

    def test_duplicate_id_rejected(self):
        data = [self.example[0], dict(self.example[0])]
        storage.DATA_FILE.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.load_schedules()

    def test_invalid_date_rejected(self):
        broken = [dict(self.example[0], due_date="2026-02-30")]
        storage.DATA_FILE.write_text(json.dumps(broken), encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.load_schedules()

    def test_failed_save_keeps_old_file(self):
        original = json.dumps(self.example, ensure_ascii=False)
        storage.DATA_FILE.write_text(original, encoding="utf-8")
        with self.assertRaises(TypeError):
            storage.save_schedules([dict(self.example[0], extra=object())])
        self.assertEqual(storage.DATA_FILE.read_text(encoding="utf-8"), original)

    def test_replace_failure_keeps_old_file(self):
        original = json.dumps(self.example, ensure_ascii=False)
        storage.DATA_FILE.write_text(original, encoding="utf-8")
        with patch.object(storage.os, "replace", side_effect=OSError("mock replacement error")):
            with self.assertRaises(OSError):
                storage.save_schedules(self.example)
        self.assertEqual(storage.DATA_FILE.read_text(encoding="utf-8"), original)
        self.assertEqual(list(storage.DATA_FILE.parent.glob(".schedules-*.tmp")), [])


    def test_boolean_schedule_id_not_matched(self):
        result = storage.mark_completed(self.example, True)
        self.assertIs(result, self.example)
        self.assertFalse(self.example[0]["completed"])

    def test_float_schedule_id_not_matched(self):
        result = storage.mark_completed(self.example, 1.0)
        self.assertIs(result, self.example)
        self.assertFalse(self.example[0]["completed"])

    def test_nan_rejected_without_overwriting_existing_file(self):
        original = json.dumps(self.example, ensure_ascii=False)
        storage.DATA_FILE.write_text(original, encoding="utf-8")
        with self.assertRaises(ValueError):
            storage.save_schedules([dict(self.example[0], extra=float("nan"))])
        self.assertEqual(storage.DATA_FILE.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
