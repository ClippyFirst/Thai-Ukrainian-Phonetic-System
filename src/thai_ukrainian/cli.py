import json
import sys
from .api import transliterate_thai

def main():
    text = " ".join(sys.argv[1:])
    if not text:
        raise SystemExit("usage: python -m thai_ukrainian.cli TEXT")
    print(json.dumps(transliterate_thai(text), ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__":
    main()
