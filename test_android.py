"""Run with: python -m unittest -v test_android."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from android_save import adapt_save
from proto_wire import encode_fields, fields


def fixture(marker=b"", version=b"1.1", slots=3):
    return encode_fields(
        [(19, 2, version)]
        + [(17, 2, encode_fields([(3, 0, i)])) for i in range(slots)]
        + ([(21, 2, marker)] if marker else [])
    )


class AndroidSaveTests(unittest.TestCase):
    def test_preserves_template_bytes_and_phone_field(self):
        template = fixture()
        phone = fixture(b"synthetic-phone-marker")
        result = adapt_save(template, phone)
        self.assertEqual(result, template + encode_fields([(21, 2, b"synthetic-phone-marker")]))
        self.assertEqual([v for n, w, v, *_ in fields(result) if n == 17],
                         [v for n, w, v, *_ in fields(template) if n == 17])

    def test_rejects_missing_duplicate_or_wrong_wire_phone_field(self):
        for phone in (fixture(), fixture(b"one") + encode_fields([(21, 2, b"two")]),
                      fixture() + encode_fields([(21, 0, 42)])):
            with self.subTest(phone=phone), self.assertRaises(ValueError):
                adapt_save(fixture(), phone)

    def test_rejects_identifier_in_distributable_template(self):
        with self.assertRaises(ValueError):
            adapt_save(fixture(b"someone-else"), fixture(b"local-phone"))

    def test_rejects_unverified_layouts(self):
        for phone in (fixture(b"phone", version=b"2.0"), fixture(b"phone", slots=2),
                      fixture(b"phone") + encode_fields([(99, 0, 1)]), b"\x0a\xff"):
            with self.subTest(phone=phone), self.assertRaises(ValueError):
                adapt_save(fixture(), phone)

    def test_cli_writes_both_files_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template = root / "template.bin"
            phone = root / "phone.bin"
            template.write_bytes(fixture())
            phone.write_bytes(fixture(b"local-phone"))
            output = root / "output"
            command = [sys.executable, str(Path(__file__).with_name("android_save.py")),
                       str(template), str(phone), str(output)]
            first = subprocess.run(command, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            expected = adapt_save(template.read_bytes(), phone.read_bytes())
            self.assertEqual((output / "Save.bin").read_bytes(), expected)
            self.assertEqual((output / "Save.temp.bin").read_bytes(), expected)
            second = subprocess.run(command, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((output / "Save.bin").read_bytes(), expected)
            self.assertEqual(phone.read_bytes(), fixture(b"local-phone"))


if __name__ == "__main__":
    unittest.main()
