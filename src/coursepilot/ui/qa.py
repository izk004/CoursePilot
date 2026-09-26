import streamlit as st

from coursepilot.exceptions import CoursePilotError


def render_qa(service) -> None:
    st.subheader("课程问答")
    question = st.text_input("你的问题", placeholder="例如：这一章最重要的三个概念是什么？")
    if st.button("检索并总结", key="ask") and question.strip():
        try:
            answer, chunks = service.answer(question)
            st.markdown(answer)
            with st.expander("查看检索到的来源片段"):
                for chunk in chunks:
                    st.markdown(f"**{chunk.filename}｜{chunk.section}**\n\n{chunk.text}")
        except CoursePilotError as exc:
            st.error(str(exc))
