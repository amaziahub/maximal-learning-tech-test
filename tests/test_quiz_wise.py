from unittest.mock import patch

import pytest
from hamcrest import assert_that

from tech_test.quiz_wize import QuizWise
from tech_test.services.timer_service import TimerService


# Mocking the QuizService to return a fixed question
def mocked_question(*args, **kwargs):
    return 1, "What is the capital of France?"


@pytest.fixture
def quizwise():
    return QuizWise()


@patch('tech_test.services.quiz_service.QuizService.get_question', new=mocked_question)
def test_game_scenario_with_session_refresh_and_timer(quizwise):
    timer_service = TimerService(quizwise.session_service)
    timer_service.run = lambda: quizwise.session_service.refresh_session()
    timer_service.run()

    session_1 = quizwise.init_session()
    session_id_1 = session_1['session_id']
    user_id_1 = "user_123"

    session_2 = quizwise.init_session()
    session_id_2 = session_2['session_id']
    user_id_2 = "user_456"

    quizwise.submit_answer(session_id_1, user_id_1, "Paris")
    quizwise.submit_answer(session_id_2, user_id_2, "Lyon")

    score_service = quizwise.get_score(session_id_1, user_id_1)
    assert_that(score_service, "Session is still ongoing, please wait.")

    timer_service.run = lambda: quizwise.session_service.refresh_session()
    timer_service.run()

    score_service = quizwise.get_score(session_id_1, user_id_1)
    assert_that(score_service,"You won! you scored: 100")

