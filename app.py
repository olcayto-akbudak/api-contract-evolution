"""Yönlü API Sözleşmesi Analizi.

Problem: API sürüm değişikliğinin mevcut istemci isteklerini veya yanıt beklentilerini kırmasını önceden görmek.
Method: İstek/yanıt uyumluluğu, değişiklik kapısı
Invariant: JSON Schema alt kümesi desteklenir; bilinmeyen anahtarlar manuel incelemeye yönlendirilir.
Boundary: Tam OpenAPI çözümleyicisi değildir; $ref, oneOf ve tüm validator semantiği ayrıca gerekir."""
SUPPORTED = {'type', 'properties', 'required', 'enum', 'minimum', 'maximum', 'items', 'additionalProperties'}

def compare(old, new, direction='request', path='$'):
    if direction not in ['request', 'response']:
        raise ValueError('direction must be request or response')
    findings = []

    def issue(kind, breaking, reason, p=path):
        findings.append({'path': p, 'change': kind, 'breaking': breaking, 'reason': reason})
    unsupported = (set(old) | set(new)) - SUPPORTED
    for key in sorted(unsupported):
        issue('UNSUPPORTED', None, f'keyword {key} requires manual review')
    ot = old.get('type')
    nt = new.get('type')
    if ot != nt:
        issue('TYPE', True, f'type {ot} -> {nt}')
        return findings
    if 'enum' in old or 'enum' in new:
        oe = set(old.get('enum', []))
        ne = set(new.get('enum', []))
        breaking = bool(ne) and (not oe or not oe <= ne) if direction == 'request' else 'enum' not in new or not ne <= oe if 'enum' in old else False
        if oe != ne:
            issue('ENUM', breaking, 'allowed values changed')
    for bound in ['minimum', 'maximum']:
        a = old.get(bound)
        b = new.get(bound)
        if a == b:
            continue
        narrower = b is not None and (a is None or (b > a if bound == 'minimum' else b < a))
        issue(bound.upper(), narrower if direction == 'request' else not narrower, 'value range changed')
    if ot == 'object':
        op = old.get('properties', {})
        np = new.get('properties', {})
        oreq = set(old.get('required', []))
        nreq = set(new.get('required', []))
        for name in sorted(oreq | nreq):
            if (name in oreq) != (name in nreq):
                issue('REQUIRED', name in nreq if direction == 'request' else name in oreq, 'requiredness changed', path + '.' + name)
        for name in sorted(op.keys() | np.keys()):
            if name not in np:
                issue('REMOVED_PROPERTY', direction == 'response' or new.get('additionalProperties') is False, 'property removed', path + '.' + name)
            elif name not in op:
                issue('ADDED_PROPERTY', direction == 'response' and old.get('additionalProperties') is False, 'new property', path + '.' + name)
            else:
                findings.extend(compare(op[name], np[name], direction, path + '.' + name))
        if old.get('additionalProperties', True) != new.get('additionalProperties', True):
            issue('ADDITIONAL_PROPERTIES', not new.get('additionalProperties', True) if direction == 'request' else not old.get('additionalProperties', True), 'unknown property policy changed')
    if ot == 'array':
        findings.extend(compare(old.get('items', {}), new.get('items', {}), direction, path + '[]'))
    return findings

def run(config):
    output = []
    for endpoint in config['endpoints']:
        changes = compare(endpoint['old'], endpoint['new'], endpoint['direction'])
        breaking = sum((x['breaking'] is True for x in changes))
        manual = sum((x['breaking'] is None for x in changes))
        output.append({'endpoint': endpoint['name'], 'direction': endpoint['direction'], 'changes': changes, 'gate': 'BLOCK' if breaking else 'REVIEW' if manual else 'PASS', 'breaking_changes': breaking})
    return {'endpoints': output, 'scope': 'Directional structural subset; not a full OpenAPI validator'}

import argparse, json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Run reproducible synthetic project scenario')
    parser.add_argument('command', choices=['demo'])
    parser.add_argument('--input', default='scenario.json')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    report = run(json.loads(Path(args.input).read_text(encoding='utf-8')))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Report: {target}')
if __name__ == '__main__':
    main()
