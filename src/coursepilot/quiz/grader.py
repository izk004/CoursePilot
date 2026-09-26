from coursepilot.llm.client import LLMClient
from coursepilot.models import QuizAttempt, QuizQuestion


class QuizGrader:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def grade(self, question: QuizQuestion, answer: str) -> QuizAttempt:
        if question.question_type == "multiple_choice":
            correct = answer.strip() == question.correct_answer.strip()
            return QuizAttempt(question_id=question.id, knowledge_point=question.knowledge_point, user_answer=answer,
                is_correct=correct, score=100 if correct else 0, feedback=question.explanation)
        result = self.llm.grade(question.prompt, question.correct_answer, answer)
        return QuizAttempt(question_id=question.id, knowledge_point=question.knowledge_point, user_answer=answer,
            is_correct=bool(result["is_correct"]), score=float(result["score"]), feedback=str(result["feedback"]))
