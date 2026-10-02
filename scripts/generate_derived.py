from pathlib import Path
import json
from thai_ukrainian.validator import validate_repository
from thai_ukrainian.source_final import build_manifest
ROOT=Path(__file__).resolve().parents[1]
report=validate_repository()
report["scope_notes"]={
"lexical_attestation":"not measured: no Thai lexicon/corpus is bundled",
"corpus_attestation":"not measured: no corpus is bundled",
"syllable_generation":"not yet claimed as lexical evidence",
"target_inventory":"external Ukrainian-Phonetic-Inventory; reproducible feature snapshot is stored locally"
}
(ROOT/"docs"/"generated-audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
manifest=build_manifest()
(ROOT/"docs"/"source-final-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(manifest,ensure_ascii=False,indent=2))
if manifest["status"] != "pass":
    raise SystemExit("source-final manifest failed")
print(json.dumps(report,ensure_ascii=False,indent=2))
