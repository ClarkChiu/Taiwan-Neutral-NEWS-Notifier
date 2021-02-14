import os
import re
import pytest
from unittest import mock
from news_notifier.BasicFuncs import BasicFuncs


def test_get_islander_news(httpserver):
    news_list_file_path = 'tests/data/islander.txt'
    with open(news_list_file_path, 'r', encoding='UTF-8') as f:
        news_list = f.read()

    webpage_path = 'tests/data/islander.html'
    with open(webpage_path, 'r', encoding='UTF-8') as f:
        httpserver.serve_content(f.read())

    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/testing.checkpoint'
    basic_func.islander_url = httpserver.url
    assert news_list == str(basic_func.get_islander_news())


def test_create_telegram_send_conf():
    basic_func = BasicFuncs()
    basic_func.create_telegram_send_conf()
    with open('telegram-send.conf', 'r') as conf_file:
        assert re.match(
            (
                r'\[telegram\]\n'
                r'token = [0-9]{10}:[a-zA-Z0-9_-]{35}\n'
                r'chat_id = [\-\@\w\_]+'
            ),
            conf_file.read()
        )


def test_create_telegram_send_conf_without_env_var():
    basic_func = BasicFuncs()
    telegram_to = os.environ['TELEGRAM_TO']

    with pytest.raises(Exception):
        del os.environ['TELEGRAM_TO']
        basic_func.create_telegram_send_conf()

    os.environ['TELEGRAM_TO'] = telegram_to


@mock.patch('news_notifier.BasicFuncs.send')
def test_send_notification(telegram_send_send_action):
    basic_func = BasicFuncs()
    basic_func.send_notification('Testing', ['123'])
    telegram_send_send_action.assert_called_once()


def test_create_checkpoint():
    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/testing.checkpoint'
    basic_func.create_checkpoint(['News', 'List'])

    with open(basic_func.checkpoint_filepath, 'r'):
        pass

    os.remove(basic_func.checkpoint_filepath)


def test_get_ptt_news(httpserver):
    news_list_file_path = 'tests/data/ptt.txt'
    with open(news_list_file_path, 'r', encoding='UTF-8') as f:
        news_list = f.read()

    webpage_path = 'tests/data/ptt.html'
    with open(webpage_path, 'r', encoding='UTF-8') as f:
        httpserver.serve_content(f.read())

    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/testing.checkpoint'
    basic_func.ptt_hot_news_url = httpserver.url
    assert news_list == str(basic_func.get_ptt_hot_news())


def test_get_mobile01_news(httpserver):
    news_list_file_path = 'tests/data/mobile01.txt'
    with open(news_list_file_path, 'r', encoding='UTF-8') as f:
        news_list = f.read()

    webpage_path = 'tests/data/mobile01.html'
    with open(webpage_path, 'r', encoding='UTF-8') as f:
        httpserver.serve_content(f.read())

    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/testing.checkpoint'
    basic_func.mobile01_hot_news_url = httpserver.url
    assert news_list == str(basic_func.get_mobile01_hot_news())


def test_get_dcard_news(httpserver):
    news_list_file_path = 'tests/data/dcard.txt'
    with open(news_list_file_path, 'r', encoding='UTF-8') as f:
        news_list = f.read()

    webpage_path = 'tests/data/dcard.html'
    with open(webpage_path, 'r', encoding='UTF-8') as f:
        httpserver.serve_content(f.read())

    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/testing.checkpoint'
    basic_func.dcard_hot_news_url = httpserver.url
    assert news_list == str(basic_func.get_dcard_hot_news())


def test_get_saved_news_exists():
    basic_func = BasicFuncs()
    basic_func.pre_checkpoint_filepath = 'checkpoint/test-01.checkpoint'
    basic_func.checkpoint_filepath = 'checkpoint/test-02.checkpoint'
    saved_news = basic_func.get_saved_news()
    assert len(saved_news) != 0


def test_get_saved_news_not_exists():
    basic_func = BasicFuncs()
    basic_func.checkpoint_filepath = 'checkpoint/test-03.checkpoint'
    saved_news = basic_func.get_saved_news()
    assert len(saved_news) == 0
