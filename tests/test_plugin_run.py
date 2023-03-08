import pytest
from unittest.mock import patch
from subprocess import CompletedProcess
from yafti.plugin.run import Run
from pydantic import ValidationError


@pytest.mark.asyncio
@patch.object(Run, "exec")
async def test_run_call_str(mock_exec):
    r = Run()
    mock_exec.return_value = CompletedProcess(
        "hello-world", returncode=0, stdout=b"", stderr=b""
    )
    await r("hello-world")
    mock_exec.assert_called_with("hello-world")


@pytest.mark.asyncio
@patch.object(Run, "exec")
async def test_run_call_list(mock_exec):
    r = Run()
    mock_exec.return_value = CompletedProcess(
        "hello-world", returncode=0, stdout=b"", stderr=b""
    )
    await r(["hello", "world"])
    mock_exec.assert_called_with("hello world")


@pytest.mark.asyncio
async def test_run_call_validation():
    r = Run()
    with pytest.raises(ValidationError):
        await r({"hello": "world"})


@pytest.mark.asyncio
async def test_run_exec():
    r = Run()
    await r.exec("ls")
