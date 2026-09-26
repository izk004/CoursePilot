from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from coursepilot.mastery.bkt import BKTParameters, update_mastery
from coursepilot.models import KnowledgePointMastery, QuizAttempt


class Base(DeclarativeBase): pass
class MasteryRow(Base):
    __tablename__ = "mastery"
    knowledge_point: Mapped[str] = mapped_column(String, primary_key=True)
    probability: Mapped[float] = mapped_column(Float)
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    last_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
class AttemptRow(Base):
    __tablename__ = "attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[str] = mapped_column(String)
    knowledge_point: Mapped[str] = mapped_column(String)
    user_answer: Mapped[str] = mapped_column(String)
    is_correct: Mapped[bool] = mapped_column(Boolean)
    score: Mapped[float] = mapped_column(Float)
    feedback: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MasteryRepository:
    def __init__(self, url: str, parameters: BKTParameters):
        self.engine, self.parameters = create_engine(url), parameters; Base.metadata.create_all(self.engine)
    def record(self, attempt: QuizAttempt) -> KnowledgePointMastery:
        with Session(self.engine) as session:
            row = session.get(MasteryRow, attempt.knowledge_point)
            if row is None: row = MasteryRow(knowledge_point=attempt.knowledge_point, probability=self.parameters.initial, attempt_count=0); session.add(row)
            row.probability = update_mastery(row.probability, attempt.is_correct, self.parameters); row.attempt_count += 1; row.last_correct = attempt.is_correct
            session.add(AttemptRow(**attempt.model_dump())); session.commit()
            return KnowledgePointMastery(knowledge_point=row.knowledge_point, probability=row.probability, attempt_count=row.attempt_count, last_correct=row.last_correct)
    def all(self) -> list[KnowledgePointMastery]:
        with Session(self.engine) as session:
            return [KnowledgePointMastery(knowledge_point=r.knowledge_point, probability=r.probability, attempt_count=r.attempt_count, last_correct=r.last_correct) for r in session.scalars(select(MasteryRow).order_by(MasteryRow.probability)).all()]
