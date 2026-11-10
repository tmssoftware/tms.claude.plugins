"""Write or check the one-line section map at the top of every skill reference file.

The map lists each `## ` section with its line range, so an agent can read only the lines it needs
instead of the whole file. Run after editing a reference:

    python scripts/update-section-maps.py          # rewrite the maps
    python scripts/update-section-maps.py --check  # exit 1 if a map is missing or stale
"""
import glob
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MARKER = '> Sections (line ranges):'


def build(lines):
    """Return the file's lines with a fresh map inserted after the title line."""
    body = [l for l in lines if not l.startswith(MARKER)]
    out = [body[0], None] + body[1:]               # map goes right after the `# ` title
    heads, fenced = [], False
    for i, l in enumerate(out):
        if l and l.startswith('```'):
            fenced = not fenced
        elif l and l.startswith('## ') and not fenced:
            heads.append(i)
    parts = []
    for n, start in enumerate(heads):
        end = (heads[n + 1] if n + 1 < len(heads) else len(out)) - 1
        title = re.sub(r'[`*]', '', out[start][3:]).strip()
        title = re.sub(r'\s*\(.*$', '', title)
        if len(title) > 48:                            # keep the map short, cut between words
            title = title[:48].rsplit(' ', 1)[0].rstrip(' ,:/-')
        parts.append(f'{start + 1}-{end + 1} {title}')
    out[1] = MARKER + ' ' + ' · '.join(parts)
    return out


def main(check):
    stale = []
    for path in sorted(glob.glob(os.path.join(ROOT, '*', 'skills', '*', 'references', '*.md'))):
        with open(path, encoding='utf-8', newline='') as f:
            text = f.read()
        eol = '\r\n' if '\r\n' in text else '\n'
        lines = text.split(eol)
        new = eol.join(build(lines))
        if new != text:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    f.write(new)
    for p in stale:
        print(('stale: ' if check else 'updated: ') + p)
    return 1 if check and stale else 0


if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv))
