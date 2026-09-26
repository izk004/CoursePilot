ANSWER_PROMPT = """你是一名严谨的大学课程助教。只能依据下列资料回答问题；若资料不足，请明确说明“资料中未提供足够信息”。请使用简洁、准确的中文概括要点，不得编造事实或来源。

资料：
{context}

问题：
{question}"""

QUIZ_PROMPT = """请根据下列章节资料生成严格的 JSON，不要添加 Markdown、代码块或其他说明。先提炼资料中的知识点，再生成恰好 5 道中文题目：3 道单项选择题和 2 道简答题。

每道题必须包含以下字段：knowledge_point（知识点）、prompt（题干）、options（选项）、correct_answer（正确答案）、explanation（中文解析）。题型由 question_type 指定：单项选择题使用 multiple_choice，简答题使用 short_answer。单项选择题必须恰好有 4 个中文选项，correct_answer 必须与其中一个选项的完整文本一致；简答题的 options 必须是空列表。所有题目、选项、答案和解析均须使用中文，并且只能依据所给资料。

请返回以下结构：{{\"questions\":[...]}}。

资料：
{context}"""

GRADE_PROMPT = """请评价学生的简答，仅输出 JSON，不要添加 Markdown、代码块或其他说明。返回格式为：{{\"is_correct\":布尔值,\"score\":0 到 100 的数字,\"feedback\":\"简短的中文反馈\"}}。请依据参考答案评分；反馈应指出回答是否正确及可改进之处。

题目：
{prompt}

参考答案：
{reference}

学生答案：
{answer}"""
