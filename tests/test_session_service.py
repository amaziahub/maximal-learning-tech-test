from unittest.mock import patch

import pytest
from hamcrest import assert_that, equal_to, has_item, is_not, instance_of, is_
from tech_test.session_service import SessionService, InvalidSessionError


@pytest.fixture(autouse=True)
def cleanup_sessions(session_service):
    session_service.sessions.clear()
    session_service.current_session = None
    yield


@pytest.fixture
def session_service():
    return SessionService()


def mocked_question(*args, **kwargs):
    return 1, "What is the capital of France?"


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_init_session(session_service):
    session_data = session_service.init_session()

    assert_that(session_data['question_id'], equal_to(1))
    assert_that(session_data['question'], equal_to("What is the capital of France?"))
    assert_that(session_data['session_id'], instance_of(str))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_session_is_stored_in_memory(session_service):
    session_data = session_service.init_session()
    session_service.init_session()
    assert_that(session_service.sessions, has_item(session_data))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_refresh_session(session_service):
    first_session = session_service.init_session()
    refreshed_session = session_service.refresh_session()

    assert_that(first_session, is_not(equal_to(refreshed_session)))
    assert_that(session_service.sessions, has_item(refreshed_session))
    assert_that(session_service.current_session, is_(refreshed_session))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_answer_question_correctly(session_service):
    session_data = session_service.init_session()
    user_id = "user_123"
    user_answer = "Paris"
    session_id = session_data['session_id']

    score = session_service.answer_question(session_id, user_id, user_answer)

    assert_that(score, equal_to(100))
    assert_that(session_service.user_scores[user_id], equal_to(100))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_answer_question_incorrectly(session_service):
    session_data = session_service.init_session()
    user_id = "user_123"
    user_answer = "London"
    session_id = session_data['session_id']

    score = session_service.answer_question(session_id, user_id, user_answer)

    assert_that(score, equal_to(0))
    assert_that(session_service.user_scores[user_id], equal_to(0))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_answer_question_with_highest_score(session_service):
    correct_answer_session_id = session_service.init_session()['session_id']
    correct_user_id = "user_123"
    correct_user_answer = "Paris"

    session_service.answer_question(correct_answer_session_id, correct_user_id, correct_user_answer)

    wrong_answer_session_id = session_service.init_session()['session_id']
    wrong_user_id = "user_456"
    wrong_user_answer = "Pariss"
    session_service.answer_question(wrong_answer_session_id, wrong_user_id, wrong_user_answer)

    assert_that(session_service.user_scores[correct_user_id], equal_to(100))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_answer_question_with_higher_score(session_service):
    close_to_correct_session_id = session_service.init_session()['session_id']
    close_to_correct_user_id = "user_123"
    close_to_correct_answer = "Pariss"

    session_service.answer_question(close_to_correct_session_id, close_to_correct_user_id, close_to_correct_answer)

    wrong_answer_session_id = session_service.init_session()['session_id']
    wrong_user_id = "user_456"
    wrong_answer = "London"
    session_service.answer_question(wrong_answer_session_id, wrong_user_id, wrong_answer)

    assert_that(session_service.user_scores[close_to_correct_user_id], equal_to(80))

    correct_answer = "Paris"
    session_service.answer_question(wrong_answer_session_id, wrong_user_id, correct_answer)

    assert_that(session_service.user_scores[wrong_user_id], equal_to(100))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_answer_question_invalid_session(session_service):

    session_service.init_session()
    user_id = "user_123"
    correct_answer = "Paris"

    invalid_session_id = "invalid_session_id"

    with pytest.raises(InvalidSessionError, match="Session not found or expired"):
        session_service.answer_question(user_id, correct_answer, invalid_session_id)
