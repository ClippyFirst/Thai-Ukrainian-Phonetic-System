from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PagesSmokeContractTests(unittest.TestCase):
    def test_deployed_title_assertions_match_split_heading_markup(self) -> None:
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")

        self.assertIn('<h1 id="page-title">', html)
        self.assertIn("Побачте, як <span>прочитати</span> тайський текст", html)
        self.assertIn("grep -Fq 'id=\"page-title\"' /tmp/deployed-index.html", workflow)
        self.assertIn("grep -Fq 'Побачте, як' /tmp/deployed-index.html", workflow)
        self.assertIn("grep -Fq 'тайський текст' /tmp/deployed-index.html", workflow)
        self.assertNotIn("grep -Fq 'Побачте, як прочитати тайський текст'", workflow)


if __name__ == "__main__":
    unittest.main()
