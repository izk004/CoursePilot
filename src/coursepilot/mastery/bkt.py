from dataclasses import dataclass


@dataclass(frozen=True)
class BKTParameters:
    initial: float = .20
    guess: float = .20
    slip: float = .10
    learn: float = .15


def update_mastery(prior: float, correct: bool, p: BKTParameters) -> float:
    observed = (prior * (1 - p.slip)) / (prior * (1 - p.slip) + (1 - prior) * p.guess) if correct else (prior * p.slip) / (prior * p.slip + (1 - prior) * (1 - p.guess))
    return min(1.0, max(0.0, observed + (1 - observed) * p.learn))
