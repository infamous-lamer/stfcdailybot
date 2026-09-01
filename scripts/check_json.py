"""Validate JSON files and reformat them to match `python -m json.tool`'s output.

`json.tool` only handles one file per invocation, so this wraps it to work
as a pre-commit hook receiving a batch of filenames.
"""

import json
import sys


def _json_tool_format(obj: object) -> str:
    return json.dumps(obj, indent=4, sort_keys=False, ensure_ascii=True) + "\n"


def main(paths: list[str]) -> int:
    failed = False
    for path in paths:
        with open(path, encoding="utf-8") as f:
            original = f.read()

        try:
            obj = json.loads(original)
        except ValueError as exc:
            print(f"{path}: invalid JSON: {exc}", file=sys.stderr)
            failed = True
            continue

        formatted = _json_tool_format(obj)
        if formatted != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"{path}: reformatted to match `python -m json.tool`", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
