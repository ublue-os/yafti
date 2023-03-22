import pytest
from yafti.screen.package.state import PackageScreenState
from pydantic import ValidationError


def test_state_set():
    state = PackageScreenState()
    state.set("hello", True)
    assert state.get("hello") is True


def test_state_set_fail():
    state = PackageScreenState()
    with pytest.raises(ValidationError):
        state.set("hello", "world")


def test_state_load():
    input = {"hello": True, "world": False}
    state = PackageScreenState()
    state.load(input)
    assert state.get("hello") is True
    assert state.get("world") is False


def test_state_from_dict():
    input = {"hello": True, "world": False}
    state = PackageScreenState.from_dict(input)
    assert state.get("hello") is True
    assert state.get("world") is False


def test_state_remove():
    state = PackageScreenState()
    state.set("kenobi", False)
    state.set("general", True)
    assert state.get("kenobi") is False
    assert state.get("general") is True
    state.remove("kenobi")
    assert state.get("kenobi") is None
    assert state.get("general") is True


def test_state_on_off():
    state = PackageScreenState()
    state.on("grievous")
    assert state.get("grievous") is True
    state.off("grievous")
    assert state.get("grievous") is False

    state.off("ani")
    assert state.get("ani") is False
    state.on("ani")
    assert state.get("ani") is True


def test_state_toggle():
    state = PackageScreenState()
    state.on("chewy")
    assert state.get("chewy") is True
    state.toggle("chewy")
    assert state.get("chewy") is False
    state.toggle("chewy")
    assert state.get("chewy") is True


def test_state_toggle_error():
    state = PackageScreenState()
    with pytest.raises(KeyError):
        state.toggle("barf")


def test_state_get_on():
    state = PackageScreenState()
    state.on("chewy")
    state.on("han")
    state.off("greedo")

    assert state.get_on() == ["chewy", "han"]
    assert state.get_on("ch") == ["chewy"]


def test_state_keys():
    state = PackageScreenState()
    state.on("AA")
    state.on("BB")
    state.off("CC")

    assert state.keys() == ["AA", "BB", "CC"]
