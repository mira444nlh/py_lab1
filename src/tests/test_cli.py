import subprocess


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Runs `python -m toolkit <args>` and returns the result."""
    return subprocess.run(
        ['python', '-m', 'toolkit', *args],
        capture_output=True,
        text=True,
        check=False,
    )


# positive tests
def test_cli_calc():
    result = run_cli('calc', '2+2')

    assert result.returncode == 0
    assert '4' in result.stdout.strip()
    assert result.stderr == ''


def test_cli_convert():
    result = run_cli('convert', '1000', '--from', 'm', '--to', 'km')

    assert result.returncode == 0
    assert '1.0' in result.stdout.strip()
    assert result.stderr == ''


def test_cli_double_minus_behind_digit():
    result = run_cli('calc', '--', '--5')

    assert result.returncode == 0
    assert '5' in result.stdout.strip()
    assert result.stderr == ''


def test_cli_help_exits_with_zero_code():
    result = run_cli('--help')

    assert result.returncode == 0
    assert 'usage' in result.stdout.lower()
    assert result.stderr == ''


# negative tests
def test_cli_calc_division_by_zero_writes_to_stderr_and_exits_2():
    result = run_cli('calc', '5/0')

    assert result.returncode == 2
    assert 'Ошибка' in result.stderr
    assert result.stdout == ''


def test_cli_convert_incompatible_units_writes_to_stderr_and_exits_2():
    result = run_cli('convert', '1', '--from', 'm', '--to', 'kg')

    assert result.returncode == 2
    assert 'Ошибка' in result.stderr
    assert result.stdout == ""


def test_cli_missing_required_argument_exits_with_code_2():
    result = run_cli('convert', '10', '--from', 'm')

    assert result.returncode == 2
    assert '--to' in result.stderr
    assert result.stdout == ''
