import pytest
from paint_calculator.api import calculate_feet, calculate_gallons_required, sanitize_input

def test_calculate_feet():
    """Test the calculate_feet function with valid inputs."""
    assert calculate_feet({'length': '10', 'width': '12', 'height': '8'}) == 960
    assert calculate_feet({'length': '5', 'width': '5', 'height': '8'}) == 200
    assert calculate_feet({'length': '20', 'width': '15', 'height': '10'}) == 3000

def test_calculate_gallons_required():
    """Test the calculate_gallons_required function with various square footages."""
    assert calculate_gallons_required({'ft': 350}) == 1
    assert calculate_gallons_required({'ft': 349}) == 0
    assert calculate_gallons_required({'ft': 351}) == 1
    assert calculate_gallons_required({'ft': 700}) == 2

def test_sanitize_input():
    """Test the sanitize_input function with various inputs."""
    assert sanitize_input('10') == 10
    assert sanitize_input('0') == 0
    assert sanitize_input('999') == 999
    assert sanitize_input('-10') == 10
    assert sanitize_input('-0') == 0
    
    assert sanitize_input('  42  ') == 42
    
    with pytest.raises(ValueError):
        sanitize_input('abc')
    with pytest.raises(ValueError):
        sanitize_input('10.5')
    with pytest.raises(ValueError):
        sanitize_input('')
    with pytest.raises(TypeError):
        sanitize_input(None)
