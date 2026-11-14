from lvgl_mpy_studio.core import i18n
from lvgl_mpy_studio.core.i18n import catalog, set_language, tr


def test_every_english_text_stays_itself_in_english():
    """"File" is also the Italian of "Files": the File menu must not become "Files"."""
    previous = i18n.language()
    try:
        set_language("en")
        assert tr("File") == "File"
        assert tr("Files") == "Files"
        assert [text for text in catalog("it") if tr(text) != text] == []
    finally:
        set_language(previous)


def test_italian_text_goes_back_to_english_and_on_to_italian():
    previous = i18n.language()
    try:
        set_language("it")
        assert tr("File") == "File"
        assert tr("Files") == "File"
        set_language("en")
        assert tr(catalog("it")["Upload Files…"]) == "Upload Files…"
    finally:
        set_language(previous)
