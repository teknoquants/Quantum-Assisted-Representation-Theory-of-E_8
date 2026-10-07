#!/usr/bin/env python3
"""Diagnostic for corrected item F2. See README.md for limits."""
import json
from validate_all import run
if __name__ == '__main__':
    result = run(['F2'])[0]
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(result['execution'] != 'PASS')
