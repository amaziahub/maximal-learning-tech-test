from hamcrest import assert_that

from tech_test.tech_test import greet_me


def test_greet():
    greet_me('Amazia')


def test_check_tech_test():
    assert_that(False)
