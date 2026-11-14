#!/usr/bin/env python3
"""Re-apply the Universal Recipes rebrand after each upstream sync (idempotent).

Protected anchors (kept intact on every run):
- LICENSE, tests/data binary fixtures (.zip)
- .github/ and scripts/ are excluded from the sweep entirely
"""
from pathlib import Path
import shutil

PAIRS = [
 ("MEALIE_", "UNIVERSALRECIPES_"),
 ("MEALIE", "UNIVERSALRECIPES"),
 ("Mealie", "UniversalRecipes"),
 ("mealie", "universalrecipes"),
]
SKIP_EXT = {".png",".jpg",".jpeg",".ico",".webp",".woff",".woff2",".ttf",".eot",".otf",".gif",".pdf",".gz",".zip",".mp4"}
KEEP = {"LICENSE", "migrate.py"}
DELETE = ["docs", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "MAINTAINERS.md",
          "SECURITY.md", "cliff.toml", "crowdin.yml", "renovate.json", ".github/FUNDING.yml",
          ".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE"]


def main():
    for d in DELETE:
        p = Path(d)
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        elif p.exists():
            p.unlink()
    for p in Path(".").rglob("*"):
        if ".git" in p.parts or not p.is_file() or p.name in KEEP or p.suffix in SKIP_EXT:
            continue
        if str(p).startswith((".github/", "scripts/")):
            continue
        try:
            t = p.read_text()
        except Exception:
            continue
        nt = t
        for a, b in PAIRS:
            nt = nt.replace(a, b)
        if nt != t:
            p.write_text(nt)
    for p in list(Path(".").rglob("*mealie*")) + list(Path(".").rglob("*Mealie*")):
        if ".git" in p.parts or p.is_dir():
            continue
        nb = p.name.replace("mealie", "universalrecipes").replace("Mealie", "UniversalRecipes")
        if nb != p.name:
            p.rename(p.with_name(nb))
    readme = Path("README.md")
    if readme.exists() and not readme.read_text().startswith("# Universal Recipes"):
        print("README drifted - rewrite needed")
    print("migrate done")


if __name__ == "__main__":
    main()
