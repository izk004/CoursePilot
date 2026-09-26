import pytest

from coursepilot.exceptions import ParsingError
from coursepilot.ingestion.parsers import parse_file


def test_parse_utf8_txt():
    sections = parse_file("notes.txt", "第一章\n\n内容".encode())
    assert sections[0].title == "文本资料"
    assert "内容" in sections[0].text


def test_rejects_unknown_extension():
    with pytest.raises(ParsingError):
        parse_file("notes.docx", b"anything")
