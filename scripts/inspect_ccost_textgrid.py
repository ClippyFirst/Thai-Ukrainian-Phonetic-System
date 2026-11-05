#!/usr/bin/env python3
"""Inspect researcher-supplied CCOST Praat long-text TextGrids without audio."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path
from thai_ukrainian.adapters.ccost import CCOST_PHONETIC_TIERS, convert_ccost_tier, parse_textgrid_long

def inspect(paths:list[Path],sample_limit:int=5)->dict:
    files=[]; failures=[]; tier_counts:Counter[str]=Counter(); converted_counts:Counter[str]=Counter()
    for path in sorted(paths):
        try:
            grid=parse_textgrid_long(path.read_text(encoding="utf-8-sig"))
            entry={"file":path.name,"duration":grid.xmax-grid.xmin,"tiers":{}}
            for tier in grid.tiers:
                labels=[item.text for item in tier.intervals if item.text.strip()]
                tier_counts[tier.name]+=len(labels)
                entry["tiers"][tier.name]={"kind":tier.kind,"interval_count":len(tier.intervals),
                    "nonempty_labels":len(labels),"samples":labels[:sample_limit]}
                if tier.name in CCOST_PHONETIC_TIERS:
                    try: converted_counts[tier.name]+=len(convert_ccost_tier(grid,tier.name))
                    except ValueError as exc: failures.append({"file":path.name,"tier":tier.name,"error":str(exc)})
            files.append(entry)
        except (OSError,UnicodeError,ValueError) as exc:
            failures.append({"file":path.name,"error":f"{type(exc).__name__}: {exc}"})
    return {"schema_version":"1.0","source":"researcher-supplied CCOST TextGrid files; no audio accessed",
        "files_inspected":len(files),"files":files,"tier_nonempty_label_counts":dict(sorted(tier_counts.items())),
        "converted_label_counts":dict(sorted(converted_counts.items())),"failures":failures,
        "limitations":["TextGrid labels are source annotations, not independent project gold.",
        "This report inspects TextGrid text only; it does not open or require WAV files.",
        "Successful conversion does not establish released-tier completeness or linguistic correctness.",
        "Only Praat long-text TextGrid is supported; short/binary formats are rejected."]}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths",nargs="+",type=Path,help="TextGrid file(s) or directories")
    parser.add_argument("--sample-limit",type=int,default=5)
    parser.add_argument("--output",type=Path,help="Optional JSON report path")
    args=parser.parse_args()
    if args.sample_limit<0: parser.error("--sample-limit must be non-negative")
    paths=[]
    for path in args.paths:
        if path.is_dir(): paths.extend(path.rglob("*.TextGrid")); paths.extend(path.rglob("*.textgrid"))
        elif path.is_file(): paths.append(path)
        else: parser.error(f"path does not exist: {path}")
    report=inspect(paths,args.sample_limit); rendered=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.output: args.output.write_text(rendered,encoding="utf-8")
    print(rendered,end="")
    return 1 if report["failures"] else 0

if __name__=="__main__": raise SystemExit(main())
