#!/bin/bash
# Offline checks — no raw data needed (pytest intentionally not required).
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
python3 "$ROOT/src/tests/test_parity.py"
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('tc', '$ROOT/src/tests/test_consistency.py')
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
tc.test_on_frozen(); tc.test_pk1_frozen(); tc.test_lift_cis_lower_above_zero(); tc.test_guardrails_present_on_pages()
print('CONSISTENCY OK')
"
git -C "$ROOT" ls-files | grep -iE '\.(xls|xlsx|csv|mp4|jpg|png|pkl|parquet)$' && { echo 'FAIL: binaries tracked'; exit 1; } || echo 'HYGIENE OK: no binaries tracked'
echo 'ALL CHECKS PASSED'
