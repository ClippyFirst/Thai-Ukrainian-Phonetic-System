from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"thai"; DOCS=ROOT/"docs"
def count(name):
    with (DATA/name).open(encoding="utf-8",newline="") as f:return sum(1 for _ in csv.DictReader(f))
def main():
    audit={
      "consonant_graphemes":count("consonants.csv"),
      "vowel_records":count("vowels.csv"),
      "tone_marks":count("tone_marks.csv"),
      "tone_categories":count("tones.csv"),
      "formal_tone_rules":count("rules.csv"),
      "provenance_sources":count("sources.csv"),
      "phonotactic_records":count("phonotactics.csv"),
      "correspondence_records":count("correspondences.csv"),
      "generated_syllable_structures":"not yet generated",
      "validated_examples":"core rule unit tests",
      "status":"research-foundation"
    }
    (DOCS/"final-audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DOCS/"final-audit.md").write_text("# Final audit\n\n"+"\n".join(f"- **{k}**: {v}" for k,v in audit.items())+"\n",encoding="utf-8")
if __name__=="__main__":main()
