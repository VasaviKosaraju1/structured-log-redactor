"""Redact configured field names in JSON Lines without printing malformed input."""
import argparse
import json
from pathlib import Path
import sys

DEFAULT_KEYS=frozenset({'password','token','authorization','api_key','secret','email'})


def redact(value, keys=DEFAULT_KEYS):
    normalized={k.casefold() for k in keys}
    def walk(node):
        if isinstance(node,dict):
            return {k:'[REDACTED]' if k.casefold() in normalized else walk(v) for k,v in node.items()}
        if isinstance(node,list): return [walk(v) for v in node]
        return node
    return walk(value)


def process(source,destination,keys=DEFAULT_KEYS):
    count=0
    for line_number,line in enumerate(source,1):
        if not line.strip(): continue
        try: value=json.loads(line)
        except ValueError: raise ValueError(f'invalid JSON at line {line_number}; input content withheld') from None
        destination.write(json.dumps(redact(value,keys),ensure_ascii=False)+'\n')
        count+=1
    return count


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--key',action='append',default=[]);a=p.parse_args()
    try:
        with Path(a.input).open(encoding='utf-8') as source:
            process(source,sys.stdout,DEFAULT_KEYS|{k.casefold() for k in a.key})
    except (OSError,ValueError,RecursionError):
        print('Redaction failed; check input JSON and file access. Partial redacted output may have been written.',file=sys.stderr);return 2
    return 0

if __name__=='__main__': sys.exit(main())
