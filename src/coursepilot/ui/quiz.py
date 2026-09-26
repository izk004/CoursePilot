import streamlit as st

from coursepilot.exceptions import CoursePilotError


def render_quiz(generator, grader, repository, sections: list[str]) -> None:
    st.subheader("章节测验")
    if not sections:
        st.info("请先上传资料。")
        return
    section = st.selectbox("选择章节", sections)
    if st.button("生成 5 道测验题", key="generate_quiz"):
        try:
            st.session_state["quiz_questions"] = generator.generate(section)
            st.session_state.pop("graded", None)
        except CoursePilotError as exc:
            st.error(str(exc))
    questions = st.session_state.get("quiz_questions", [])
    if not questions:
        return
    answers: dict[str, str] = {}
    with st.form("quiz_form"):
        for i, q in enumerate(questions, 1):
            st.markdown(f"**{i}. {q.prompt}**  \n知识点：`{q.knowledge_point}`")
            if q.question_type == "multiple_choice":
                answers[q.id] = st.radio("选择答案", q.options, key=q.id, index=None)
            else:
                answers[q.id] = st.text_area("你的回答", key=q.id)
        submitted = st.form_submit_button("提交并评分")
    if submitted:
        attempts = []
        try:
            for q in questions:
                if not answers[q.id]:
                    raise CoursePilotError("请完成所有题目后再提交。")
                attempts.append(grader.grade(q, answers[q.id]))
            for attempt in attempts:
                repository.record(attempt)
            st.session_state["graded"] = attempts
        except CoursePilotError as exc:
            st.error(str(exc))
    for attempt in st.session_state.get("graded", []):
        st.write(f"{'✅' if attempt.is_correct else '❌'} **{attempt.knowledge_point}**：{attempt.score:.0f} 分 — {attempt.feedback}")
