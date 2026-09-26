from coursepilot.mastery.bkt import BKTParameters
from coursepilot.mastery.repository import MasteryRepository
from coursepilot.models import QuizAttempt


def test_attempts_persist_between_repository_instances(tmp_path):
    url = f"sqlite:///{tmp_path / 'history.db'}"
    attempt = QuizAttempt(question_id="q1", knowledge_point="贝叶斯公式", user_answer="A", is_correct=True, score=100)
    first = MasteryRepository(url, BKTParameters())
    saved = first.record(attempt)
    second = MasteryRepository(url, BKTParameters())
    rows = second.all()
    assert len(rows) == 1
    assert rows[0].knowledge_point == "贝叶斯公式"
    assert rows[0].probability == saved.probability
    assert rows[0].attempt_count == 1
