import pytest
from hamcrest import assert_that, has_entry

from tech_test.services.quiz_service import QuizService


@pytest.fixture
def quiz():
    return QuizService()


def test_get_question(quiz):
    question_id, question = quiz.get_question()
    has_entry(question_id, quiz.QUESTIONS)
    assert_that(question, quiz.QUESTIONS[question_id]["question"])


@pytest.mark.parametrize("question_id, answer, expected_score", [
    (1, "Paris", 100),
    (1, "paris", 100),
    (1, "Parisss", 80),  # Close match
    (1, "London", 0),
    (2, "7", 100),
    (3, "Au", 100),
    (3, "AG", 0),
    (4, "Shakespeare", 100),
    (4, "shakespear", 80),  # Close match
    (5, "4", 100),
    (5, "Four", 0),
])
def test_check_answer(quiz, question_id, answer, expected_score):
    assert quiz.check_answer(question_id, answer) == expected_score
