from unittest.mock import patch

import pytest
from hamcrest import assert_that, equal_to, has_item, is_not, instance_of, is_
from tech_test.session_service import SessionService


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
def test_session_replacement(session_service):
    first_session = session_service.init_session()
    second_session = session_service.init_session()

    assert_that(first_session, is_not(equal_to(second_session)))
    assert_that(session_service.sessions, has_item(first_session))
    assert_that(session_service.current_session, is_(second_session))


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_refresh_session():
    session_service = SessionService()
    first_session = session_service.init_session()
    refreshed_session = session_service.refresh_session()

    assert_that(first_session, is_not(equal_to(refreshed_session)))
    assert_that(session_service.sessions, has_item(refreshed_session))
    assert_that(session_service.current_session, is_(refreshed_session))
