#!/bin/bash
# Demo: full product path in one command (tests + gates + pointers).
# Offline except raw-data gates. Fails loudly on any mismatch.
set -eo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
bash "$ROOT/run_tests.sh"
python3 "$ROOT/triage/prospective.py" --section on --survey 2021 --check | tail -n 1
python3 "$ROOT/triage/prospective.py" --section pk1 --survey 2022 --check | tail -n 1
echo "--- shipped numbers ---"
python3 -c "
import json
for t,f in [('ON','triage/triage_demo.json'),('PK1','triage/triage_pk1.json'),('SRTO','triage/triage_srto.json')]:
    d=json.load(open('$ROOT/'+f)); print(t,'AP=%.4f base=%.4f'%(d['AP'],d['base']))"
echo "--- open: triage/triage_demo.html triage/triage_pk1.html triage/triage_srto.html ---"
echo "--- method: docs/ | history: PROGRESS.md | recalibrate: docs/PROSPECTIVE_RUNBOOK.md ---"
echo "DEMO OK"
