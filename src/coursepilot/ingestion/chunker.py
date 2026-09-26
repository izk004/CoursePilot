import re
from uuid import uuid5, NAMESPACE_URL
from coursepilot.models import DocumentChunk, ParsedSection

HEADING = re.compile(r"^(#{1,6}\s+.+|第[一二三四五六七八九十\d]+[章节部分].*|\d+(?:\.\d+)*\s+.+)$", re.M)


def _pieces(text: str, size: int, overlap: int) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    output: list[str] = []
    buffer = ""
    for paragraph in paragraphs:
        if len(buffer) + len(paragraph) + 1 <= size:
            buffer = f"{buffer}\n{paragraph}".strip(); continue
        if buffer: output.append(buffer)
        while len(paragraph) > size:
            cut = max(paragraph.rfind("。", 0, size), paragraph.rfind(". ", 0, size), size)
            output.append(paragraph[:cut].strip())
            paragraph = paragraph[max(0, cut - overlap):].strip()
        buffer = paragraph
    if buffer: output.append(buffer)
    return output


def chunk_sections(sections: list[ParsedSection], document_id: str, filename: str, document_type: str,
                   size: int = 900, overlap: int = 120) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    number = 0
    for source_index, source in enumerate(sections, 1):
        current_title = source.title
        split = HEADING.split(source.text)
        blocks: list[tuple[str, str]] = []
        for part in split:
            if not part.strip(): continue
            if HEADING.match(part.strip()): current_title = part.strip().lstrip("#").strip()
            else: blocks.append((current_title, part.strip()))
        if not blocks: blocks = [(current_title, source.text)]
        for title, block in blocks:
            for text in _pieces(block, size, overlap):
                number += 1
                chunk_id = str(uuid5(NAMESPACE_URL, f"{document_id}:{number}:{text}"))
                chunks.append(DocumentChunk(id=chunk_id, text=text, document_id=document_id, filename=filename,
                    document_type=document_type, section=title, section_index=source_index, location=source.location))
    return chunks
