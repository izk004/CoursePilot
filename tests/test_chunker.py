from coursepilot.ingestion.chunker import chunk_sections
from coursepilot.models import ParsedSection


def test_chunker_preserves_source_metadata_and_heading():
    chunks = chunk_sections([ParsedSection(title="第 1 页", text="# 概率论\n\n随机变量是核心概念。", location=1)], "doc", "a.pdf", "pdf", 100, 10)
    assert len(chunks) == 1
    assert chunks[0].section == "概率论"
    assert chunks[0].filename == "a.pdf"
    assert chunks[0].location == 1


def test_chunker_splits_long_paragraph():
    chunks = chunk_sections([ParsedSection(title="文本", text="甲" * 210, location=1)], "doc", "a.txt", "txt", 100, 10)
    assert len(chunks) >= 2
    assert all(chunk.text for chunk in chunks)
