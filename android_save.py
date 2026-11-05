"""Adapt a Steam save template using a local Android save.

Usage: python android_save.py TEMPLATE_SAVE_BIN PHONE_SAVE_BIN NEW_OUTPUT_DIRECTORY
The inputs are never modified. The output directory must not already exist.
"""

import argparse
import hashlib
from pathlib import Path

from proto_wire import fields


def adapt_save(template, phone):
    """Keep every template byte and append the phone's original field 21."""
    source = fields(template)
    mobile = fields(phone)
    if any(n == 21 for n, *_ in source):
        raise ValueError("template must not contain another device's field 21")
    markers = [(w, v, start, end) for n, w, v, start, end in mobile if n == 21]
    if len(markers) != 1 or markers[0][0] != 2 or not markers[0][1]:
        raise ValueError("phone save must contain exactly one nonempty length-delimited field 21")
    source_version = [(w, v) for n, w, v, *_ in source if n == 19]
    mobile_version = [(w, v) for n, w, v, *_ in mobile if n == 19]
    if source_version != [(2, b"1.1")] or mobile_version != source_version:
        raise ValueError("only matching field-19 format markers of 1.1 were tested")
    for nodes in (source, mobile):
        slots = [(w, v) for n, w, v, *_ in nodes if n == 17]
        if len(slots) != 3 or any(w != 2 for w, v in slots):
            raise ValueError("only the three-slot layout was tested")
        for w, payload in slots:
            fields(payload)
    extra = {n for n, *_ in mobile} - {n for n, *_ in source} - {21}
    if extra:
        raise ValueError(f"unverified phone-only top-level fields: {sorted(extra)}")
    _, _, start, end = markers[0]
    return template + phone[start:end]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("phone", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        result = adapt_save(args.template.read_bytes(), args.phone.read_bytes())
        # A new directory prevents either input or an existing save from being overwritten.
        args.output.mkdir(parents=True, exist_ok=False)
        for name in ("Save.bin", "Save.temp.bin"):
            (args.output / name).write_bytes(result)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print("Created Save.bin and Save.temp.bin; retained the local phone's field 21.")
    print(f"SHA256: {hashlib.sha256(result).hexdigest()}")


if __name__ == "__main__":
    main()
