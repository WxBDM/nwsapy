
from nwsapy.core import data_validator as dv

def test_area():
    assert dv.is_valid_area('KS') == True
    assert dv.is_valid_area('Alaska') == True
    assert dv.is_valid_area('FLORIDA') == True
    assert dv.is_valid_area('ny') == True
    assert dv.is_valid_area('NeBrAsKa') == True
    assert dv.is_valid_area('iA') == True

def test_invalid_area():
    assert dv.is_valid_area('Flo-rida') == False
    assert dv.is_valid_area('abc') == False
    assert dv.is_valid_area('') == False

# expand upon this at a much later time, handle different data types
# in validation.py.