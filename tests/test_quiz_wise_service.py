import pytest
from hamcrest import assert_that, has_entry

from tech_test.quiz_service import QuizService


@pytest.fixture
def quiz():
    return QuizService()


def test_get_question(quiz):
    question_id, question = quiz.get_question()
    has_entry(question_id, quiz.QUESTIONS)
    assert_that(question, quiz.QUESTIONS[question_id]["question"])