import hashlib

import streamlit as st

from coursepilot.exceptions import CoursePilotError
from coursepilot.ingestion.chunker import chunk_sections
from coursepilot.ingestion.parsers import parse_file


def render_upload(store, settings) -> None:
    st.subheader("上传课程资料")
    uploads = st.file_uploader("支持 PDF、PPTX、TXT", type=["pdf", "pptx", "txt"], accept_multiple_files=True)
    if not uploads:
        return
    for upload in uploads:
        data = upload.getvalue()
        document_id = hashlib.sha256(data).hexdigest()
        if store.document_exists(document_id):
            st.info(f"{upload.name} 已入库，已跳过重复文件。")
            continue
        try:
            sections = parse_file(upload.name, data)
            chunks = chunk_sections(sections, document_id, upload.name, upload.name.rsplit(".", 1)[-1].lower(), settings.chunk_size, settings.chunk_overlap)
            store.add(chunks)
            st.success(f"{upload.name}：解析 {len(sections)} 个页面/幻灯片，写入 {len(chunks)} 个片段。")
        except CoursePilotError as exc:
            st.error(f"{upload.name}：{exc}")
    sections = store.sections()
    if sections:
        st.caption("已发现章节：" + "、".join(sections))
