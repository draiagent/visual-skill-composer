#!/usr/bin/env python3
"""Validate VSC project manifests against schemas/project-manifest.schema.json.

Usage:  python tools/validate.py [file ...]     (defaults to examples/*)
"""
import glob
import io
import json
import sys

try:
    import jsonschema
except ImportError:
    sys.exit("pip install jsonschema")

try:
    import yaml
except ImportError:
    yaml = None

SCHEMA = "schemas/project-manifest.schema.json"


def load(path):
    text = io.open(path, encoding="utf-8").read()
    if path.endswith((".yaml", ".yml")):
        if yaml is None:
            sys.exit("pip install pyyaml to validate YAML manifests")
        return yaml.safe_load(text)
    return json.loads(text)


def main(argv):
    paths = argv or sorted(glob.glob("examples/*.vsc.*"))
    schema = json.load(io.open(SCHEMA, encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    failed = 0
    for path in paths:
        errors = sorted(validator.iter_errors(load(path)), key=lambda e: list(e.path))
        if errors:
            failed += 1
            print("FAIL " + path)
            for err in errors:
                print("     " + "/".join(str(p) for p in err.path) + ": " + err.message)
        else:
            print("OK   " + path)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
