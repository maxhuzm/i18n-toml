"""
Tests for i18n_toml library.
"""

import tomllib
from pathlib import Path
import pytest
from i18n_toml import *

EXAMPLES = Path(__file__).parent.parent / "examples"
LOCALE_RU = "ru"
LOCALE_EN = "en"
LOCALE_EMPTY = "empty"


def test_ru_buttons():
    """Test button text in ru locale."""
    file_path = EXAMPLES / LOCALE_RU / "buttons.toml"
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    assert data["login_btn"] == "Войти"


def test_ru_messages():
    """Test message text in ru locale."""
    file_path = EXAMPLES / LOCALE_RU / "messages.toml"
    username = "Рудольфо"
    with open(file_path, "rb") as f:
        data = tomllib.load(f)
    assert data["info"]["welcome"].format(username=username) == f"Добро пожаловать, {username}!"


def test_i18ntoml_messages():
    """Test I18nToml example messages."""
    i18n = I18nToml(EXAMPLES, LOCALE_RU)
    username = "Рудольфо"
    version = "1.0.1"
    assert i18n.get("messages.info.welcome").format(username=username) == "Добро пожаловать, Рудольфо!"
    assert i18n.get("messages.info.version.stable").format(version=version) == "Стабильная версия приложения: 1.0.1"


def test_i18ntoml_buttons():
    """Test I18nToml example buttons."""
    i18n = I18nToml(EXAMPLES, LOCALE_RU)
    assert i18n.get("buttons.login_btn") == "Войти"
    assert i18n.get("buttons.logout_btn") == "Выйти"
    assert i18n.get("buttons.cancel_btn") == "Отмена"


def test_i18ntoml_exceptions():
    """Test I18nToml exceptions."""
    with pytest.raises(NotADirectoryError):
        I18nToml(EXAMPLES, "fr")
    with pytest.raises(FileNotFoundError):
        i18n = I18nToml(EXAMPLES, LOCALE_RU)
        i18n.get("not_exist_file.key")
    with pytest.raises(KeyError):
        i18n = I18nToml(EXAMPLES, LOCALE_RU)
        i18n.get("buttons.not_exist_key")
    with pytest.warns(UserWarning):
        i18n = I18nToml(EXAMPLES, LOCALE_EMPTY)


def test_i18ntoml_functor():
    """Test I18nToml object as functor."""
    i18n = I18nToml(EXAMPLES, LOCALE_RU)
    username = "Рудольфо"
    assert i18n("messages.info.welcome").format(username=username) == "Добро пожаловать, Рудольфо!"
    assert i18n("buttons.login_btn") == "Войти"
