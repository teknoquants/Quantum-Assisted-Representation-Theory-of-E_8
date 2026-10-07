#!/usr/bin/env python3
"""Run both preserved suites against the consolidated paper. Diagnostics are not proofs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--document', type=Path, default=ROOT / 'merged_paper.docx')
    parser.add_argument('--output', type=Path, default=ROOT / 'merged_results.json')
    args = parser.parse_args()
    document = args.document.resolve()
    manifest = json.loads((ROOT / 'merged_manifest.json').read_text())
    with ZipFile(document) as archive:
        tree = ET.fromstring(archive.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs = [''.join(t.text or '' for t in p.findall('.//w:t', ns))
                  for p in tree.findall('.//w:p', ns)]
    if not paragraphs.index('Abstract') < paragraphs.index('Introduction'):
        raise ValueError('Abstract must precede Introduction')
    for group in ('intro', 'bibliography'):
        for paragraph in manifest[group]:
            if paragraph not in paragraphs:
                raise ValueError(f'Merged {group} mismatch: {paragraph[:100]}')
    payload = {
        'meaning': 'PASS means finite diagnostics and document synchronization succeeded, not a general proof or hardware certification.',
        'document_sha256': hashlib.sha256(document.read_bytes()).hexdigest(),
        'introduction_paragraphs_matched': len(manifest['intro']),
        'bibliography_entries_matched': len(manifest['bibliography']),
        'suites': {}, 'results': []}
    with tempfile.TemporaryDirectory() as temporary:
        for suite, count in manifest['expected_suite_checks'].items():
            output = Path(temporary) / (suite + '.json')
            run = subprocess.run([sys.executable, str(ROOT / suite / 'validate_all.py'),
                                  '--document', str(document), '--output', str(output)],
                                 capture_output=True, text=True)
            if run.returncode:
                raise RuntimeError(f'{suite} failed:\n{run.stdout}\n{run.stderr}')
            report = json.loads(output.read_text())
            if len(report['results']) != count or any(r['execution'] != 'PASS' for r in report['results']):
                raise ValueError(f'{suite}: unexpected count or failed diagnostic')
            payload['suites'][suite] = {k:v for k,v in report.items() if k != 'results'}
            for row in report['results']:
                payload['results'].append(dict(row, id=suite + '/' + row['id']))
            print(f'{suite}: {count} diagnostics PASS; document synchronized')
    payload['diagnostic_count'] = len(payload['results'])
    payload['execution'] = 'PASS'
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    print(f"Total: {payload['diagnostic_count']} diagnostic groups; introduction and bibliography synchronized")

if __name__ == '__main__':
    main()
