#!/usr/bin/env python3
"""Read-only checks for changed Markdown; run from a Git repository."""
import argparse
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


def git(*args):
    return subprocess.check_output(['git', *args], text=True).splitlines()


def anchors(path):
    result=set(); counts={}; fenced=False
    for line in path.read_text().splitlines():
        if line.lstrip().startswith('```'):
            fenced=not fenced
        if fenced: continue
        m=re.match(r'^#{1,6}\s+(.+)', line)
        if m:
            title=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',m[1])
            slug=re.sub(r'[^\w\- ]','',title.lower()).replace(' ','-')
            count=counts.get(slug,0); counts[slug]=count+1
            result.add(slug if count==0 else f'{slug}-{count}')
        result.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)',line))
    return result


def check(path):
    errors=[]; fenced=False; blank=False; width=None
    for num,line in enumerate(path.read_text().splitlines(),1):
        if re.match(r'^(<<<<<<< |=======\s*$|>>>>>>> )',line):
            errors.append((num,'merge marker'))
        if line.lstrip().startswith('```'):
            fenced=not fenced; blank=False; width=None; continue
        if fenced: continue
        if not line.strip():
            if blank:errors.append((num,'consecutive blank lines'))
            if line:errors.append((num,'whitespace-only line'))
            blank=True; width=None; continue
        blank=False
        if line.startswith('|') and line.endswith('|'):
            cells=len(re.split(r'(?<!\\)\|',line))-2
            if width is not None and cells!=width:errors.append((num,'inconsistent table columns'))
            width=cells
        else:width=None
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',line):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
            target=unquote(target); dest,_,fragment=target.partition('#')
            resolved=(path.parent/dest) if dest else path
            if not resolved.exists():errors.append((num,f'missing file: {target}'))
            elif fragment and resolved.suffix=='.md' and fragment not in anchors(resolved):
                errors.append((num,f'missing heading: {target}'))
    return errors


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='origin/main');args=parser.parse_args()
    paths=set(git('diff','--name-only',f'{args.base}...HEAD'))
    paths.update(git('diff','--name-only','HEAD'))
    paths.update(git('ls-files','--others','--exclude-standard'))
    failed=0;checked=0
    for name in sorted(paths):
        path=Path(name)
        if path.suffix!='.md' or not path.is_file():continue
        checked+=1
        for line,error in check(path):
            print(f'{name}:{line}: {error}');failed+=1
    print(f'{checked} Markdown files checked; {failed} errors')
    return bool(failed)


if __name__=='__main__':raise SystemExit(main())
