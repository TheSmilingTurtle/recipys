import time
from pathlib import Path

import pytest

from recipys.ConfigFile import ConfigFile
from utility_fixtures import config_file_cleanup


def test_ConfigFile_construction():
    config_file = ConfigFile()
    assert config_file.file_name == "config.json"
    assert config_file.user_agent == (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
        "Gecko/20100101 Firefox/89.0"
    )
    assert config_file.headers == {
        "User-Agent": config_file.user_agent,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml"
            ";q=0.9,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.duckduckgo.com/",
    }
    assert config_file.last_request - time.time() < 1


def test_create_and_read_config_file(config_file_cleanup):
    config_file = ConfigFile()
    assert not Path(config_file.file_name).is_file()

    # File does not exist -> create with default values
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()

    config_file.user_agent = "test_user_agent"
    config_file.headers["User-Agent"] = config_file.user_agent
    new_time = time.time() + 10
    config_file.last_request = new_time

    # File exists -> instance variables overwritten with file content
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()
    assert not config_file.user_agent == "test_user_agent"
    assert not config_file.headers["User-Agent"] == "test_user_agent"
    assert not config_file.last_request == new_time


def test_tampered_config_file_headers(config_file_cleanup):
    config_file = ConfigFile()
    assert config_file.headers.get("User-Agent", None)

    # File does not exist -> create with current values
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()

    # Change content of instance
    del config_file.headers["User-Agent"]
    assert not config_file.headers.get("User-Agent", None)

    # File exists but differs from local info -> reset content
    assert not config_file.headers.get("User-Agent", None)
    config_file._read_config_file()

    # Local instance should be updated with config file's content
    assert config_file.headers["User-Agent"]


def test_tampered_config_file_last_request(config_file_cleanup):
    config_file = ConfigFile()

    # File does not exist -> create with current values
    config_file._read_config_file()
    assert Path(config_file.file_name).is_file()

    # Change content of instance
    assert config_file.last_request
    config_file.last_request = "not_a_number"

    # File exists but local info is invalid -> reset content
    config_file._read_config_file()

    # Local instance should be updated with config file's content
    assert config_file.last_request

    # Change content of instance
    config_file.last_request = str(time.time() - 10)

    # File exists but local info is invalid -> reset content
    config_file._read_config_file()

    # Local instance should be updated with config file's content
    assert config_file.last_request


def test_get_delta_last_request(config_file_cleanup):
    config_file = ConfigFile()
    config_file._read_config_file()

    time.sleep(0.1)
    delta = config_file.get_delta_last_request()
    assert 0.1 < delta

    time.sleep(0.1)
    delta = config_file.get_delta_last_request()
    assert 0.15 < delta


def test_update_time_last_request(config_file_cleanup):
    config_file = ConfigFile()
    timestamp_initial = config_file.last_request
    config_file._read_config_file()

    time.sleep(0.1)
    config_file.update_time_last_request()
    assert 0.1 < time.time() - timestamp_initial

    time.sleep(0.1)
    config_file.update_time_last_request()
    assert 0.2 < time.time() - timestamp_initial


def test_last_request_tampered_in_json_file():
    config_file = ConfigFile()

    config_file.last_request = time.time() - 1000
    last_request_in_config_file = {"last_request": time.time()}

    with pytest.raises(KeyError):
        config_file._get_last_request_from_json_file(
            last_request_in_config_file
        )
