import core.utils as utils
import time

def test_get_current_year():
    expected = int(time.strftime("%Y", time.localtime()))
    assert utils.get_current_year() == expected

def test_get_current_date():
    expected = time.strftime("%Y-%m-%d", time.localtime())
    assert utils.get_current_date() == expected
