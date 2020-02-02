from aliasci import *
import pytest


def test_check_toml_ok():
    load_toml_config('[all]\ngs = "git status"\n[bash]\ngaap = "sdfs"')


def test_check_toml_wrong():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        load_toml_config('[NotSUpported]\ngs = "git status"\n')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
