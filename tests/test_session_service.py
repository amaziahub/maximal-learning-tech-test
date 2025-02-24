from unittest.mock import patch

from hamcrest import assert_that, equal_to, has_entry, is_not

from tech_test.session_service import SessionService


def mocked_question(*args, **kwargs):
    return 1, "What is the capital of France?"


@patch('tech_test.quiz_service.QuizService.get_question', new=mocked_question)
def test_init_session_for_user():
    user_id = "user_123"
    session_service = SessionService()
    session_data = session_service.init_session_for_user(user_id)

    assert_that(session_data['user_id'], user_id)
    assert_that(session_data['question_id'], 1)
    assert_that(session_data['question'], "What is the capital of France?")
    assert isinstance(session_data['session_id'], str)


def test_multiple_users():
    user_id_1 = "user_123"
    user_id_2 = "user_456"

    session_service = SessionService()

    session_data_1 = session_service.init_session_for_user(user_id_1)
    session_data_2 = session_service.init_session_for_user(user_id_2)

    assert_that(session_data_1['user_id'], equal_to(user_id_1))
    assert_that(session_data_2['user_id'], equal_to(user_id_2))

    assert_that(session_data_1['session_id'], is_not(equal_to(session_data_2['session_id'])))
    assert_that(session_data_1['user_id'], is_not(equal_to(session_data_2['user_id'])))


def test_session_is_stored_in_memory():
    user_id = "user_123"

    session_service = SessionService()
    session_data = session_service.init_session_for_user(user_id)

    has_entry(session_service.sessions, user_id)
    assert_that(session_service.sessions[user_id], session_data)
