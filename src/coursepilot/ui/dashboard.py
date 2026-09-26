import streamlit as st


def render_dashboard(repository) -> None:
    st.subheader("掌握度看板")
    rows = repository.all()
    if not rows:
        st.info("完成至少一道测验题后，这里会展示掌握度和复习建议。")
        return
    st.dataframe([{"知识点": r.knowledge_point, "掌握概率": f"{r.probability:.1%}", "答题次数": r.attempt_count,
                   "最近结果": "正确" if r.last_correct else "错误"} for r in rows], use_container_width=True, hide_index=True)
    st.markdown("#### 最该复习的 3 个知识点")
    for i, row in enumerate(rows[:3], 1):
        st.write(f"{i}. **{row.knowledge_point}**（{row.probability:.1%}）— 先回顾概念，再完成针对性练习。")
    st.caption("建议按以上由低到高的掌握概率依次复习；每复习一个知识点后重做相关题目。")
