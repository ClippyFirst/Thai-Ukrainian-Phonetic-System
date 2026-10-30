from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_browser_ipa_output_uses_explicit_language_and_font_fallback():
    css = (ROOT / "web" / "src" / "styles.css").read_text(encoding="utf-8")
    app = (ROOT / "web" / "src" / "app.js").read_text(encoding="utf-8")
    assert '[lang="und-fonipa"]' in css
    for font in ('"Charis SIL"', '"Doulos SIL"', '"DejaVu Sans"'):
        assert font in css
    for feature in ('"ccmp"', '"mark"', '"mkmk"'):
        assert feature in css
    assert "unicode-bidi: isolate" in css
    assert "ipa-output" in app
    assert 'lang="und-fonipa"' in app
    assert "@import" not in css.lower()
    assert "url(http" not in css.lower()


def test_ipa_output_is_escaped_before_rendering():
    app = (ROOT / "web" / "src" / "app.js").read_text(encoding="utf-8")
    assert "esc(v)" in app
    assert "a.phonemicIpa" in app and "a.phoneticIpa" in app
