#!/usr/bin/env python3
"""Copy the live dataset at https://cinchstack.com/data/ into this repository.

Downloads the three files the site serves, checks they are complete, and rebuilds
README.md and CITATION.cff from the templates in scripts/. The workflow in
.github/workflows/sync.yml runs it daily and commits whatever changed.
"""
import csv
import datetime
import io
import json
import pathlib
import sys
import urllib.request

SITE = 'https://cinchstack.com/data/'
FILES = ['pricing.csv', 'scenarios.csv', 'pricing.json']
ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).resolve().parent


def fetch(name):
    req = urllib.request.Request(SITE + name, headers={'User-Agent': 'cinchstack-data-sync'})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            sys.exit(f'{name}: HTTP {r.status}')
        return r.read()


def csv_rows(data, name):
    rows = list(csv.DictReader(io.StringIO(data.decode('utf-8'))))
    if len(rows) < 10:
        sys.exit(f'{name}: only {len(rows)} rows, refusing to overwrite the copy')
    return len(rows)


def fill(template, values):
    text = (HERE / template).read_text(encoding='utf-8')
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', value)
    if '{{' in text:
        sys.exit(f'{template} still has an unfilled {{{{placeholder}}}}')
    return text


def main():
    files = {name: fetch(name) for name in FILES}
    meta = json.loads(files['pricing.json'])
    tools = meta.get('tools') or []
    if len(tools) < 10:
        sys.exit(f'pricing.json: only {len(tools)} tools, refusing to overwrite the copy')
    checked = datetime.date.fromisoformat(meta['lastChecked'])
    values = {
        'tools': str(len(tools)),
        'plans': str(csv_rows(files['pricing.csv'], 'pricing.csv')),
        'scenarios': str(csv_rows(files['scenarios.csv'], 'scenarios.csv')),
        'lastChecked': f'{checked.day} {checked:%B %Y}',
        'lastCheckedIso': checked.isoformat(),
    }
    for name, data in files.items():
        (ROOT / name).write_bytes(data)
    (ROOT / 'README.md').write_text(fill('README.template.md', values), encoding='utf-8')
    (ROOT / 'CITATION.cff').write_text(fill('CITATION.template.cff', values), encoding='utf-8')
    print(f"Copied {values['tools']} tools, {values['plans']} plans and {values['scenarios']} scenarios (last checked {checked}).")


if __name__ == '__main__':
    main()
