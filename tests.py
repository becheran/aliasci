from unittest import TestCase
from aliasci import *


class Test(TestCase):

    def test_check_toml_ok(self):
        load_toml_config('[all]\ngs = "git status"\n[bash]\ngaap = "sdfs"')

    def test_check_toml_wrong(self):
        with self.assertRaises(SystemExit):
            load_toml_config('[NotSUpported]\ngs = "git status"\n')
