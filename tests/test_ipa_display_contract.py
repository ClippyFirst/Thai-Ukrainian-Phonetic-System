from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_browser_ipa_output_uses_explicit_language_and_font_fallback():
    css = (ROOT / "web" / "src" / "styles.css").read_text(encoding="utf-8")
    app = (ROOT / "web" / "src" / "app.js").read_text(encoding="utf-8")
    assert '.ipa-output{' in css
    for font in ('"Charis SIL"', '"Doulos SIL"', '"DejaVu Sans"'):
        assert font in css
    for feature in ('"ccmp"', '"mark"', '"mkmk"'):
        assert feature in css
    assert "unicode-bidi:isolate" in css
    assert "ipa-output" in app
    assert 'lang="und-fonipa"' in app
    assert "@import" not in css.lower()
    assert "url(http" not in css.lower()


def test_fastthaig2p_api_result_fields_are_escaped_before_rendering():
    app = (ROOT / "web" / "src" / "app.js").read_text(encoding="utf-8")
    assert "const esc = value =>" in app
    for expression in (
        "esc(syllable.raw_ipa)",
        "esc(syllable.ipa || '—')",
        "esc(syllable.ukrainian || '—')",
        "esc(word.thai)",
        "esc(result.ukrainian)",
        "esc(result.raw_ipa)",
        "esc(result.upstream_commit)",
    ):
        assert expression in app, f"unescaped API result field: {expression}"
    assert "output.innerHTML =" in app
    assert "analysis.phonemicIpa" not in app and "analysis.phoneticIpa" not in app
