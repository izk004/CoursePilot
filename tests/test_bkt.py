from coursepilot.mastery.bkt import BKTParameters, update_mastery


def test_correct_answer_increases_mastery():
    parameters = BKTParameters()
    assert update_mastery(.20, True, parameters) > .20


def test_wrong_answer_reduces_mastery_and_bounds_probability():
    parameters = BKTParameters()
    result = update_mastery(.20, False, parameters)
    assert 0 <= result < .20 <= 1
    assert 0 <= update_mastery(.999, True, parameters) <= 1
