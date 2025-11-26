import pytest
import json

from paint_calculator.run import app

def test_index_route(client):
    """Test the index route returns a 200 status code and contains the expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Calculating Paint Required' in response.data
    assert b'Enter the number of rooms' in response.data

def test_dimensions_route_valid_input(client):
    """Test the dimensions route with valid input."""
    response = client.get('/dimensions?rooms=2')
    assert response.status_code == 200
    # Check for actual content - the page shows "Calculating Paint Required" header
    assert b'Calculating Paint Required' in response.data
    # Check that we have room number cells (1 and 2)
    assert b'<td>\n                1\n            </td>' in response.data
    assert b'<td>\n                2\n            </td>' in response.data

def test_dimensions_route_negative_input(client):
    """Test the dimensions route with negative input (should be converted to positive)."""
    response = client.get('/dimensions?rooms=-2')
    assert response.status_code == 200
    # Check that we have room cells (showing as numbers 1 and 2 in table)
    assert b'<td>\n                1\n            </td>' in response.data
    assert b'<td>\n                2\n            </td>' in response.data

def test_dimensions_route_invalid_input(client):
    """Test the dimensions route with invalid input - should redirect with flash message."""
    response = client.get('/dimensions?rooms=abc', follow_redirects=True)
    # Should redirect to index page
    assert response.status_code == 200
    assert b'Enter the number of rooms' in response.data

def test_results_route_valid_input(client):
    """Test the results route with valid form data."""
    form_data = {
        'length-0': '10',
        'width-0': '12',
        'height-0': '8',
        'length-1': '15',
        'width-1': '10',
        'height-1': '9'
    }
    response = client.post('/results', data=form_data)
    assert response.status_code == 200
    assert b'Paint Calculation Results' in response.data
    # Check that the JSON data contains our room data
    assert b'room-1' in response.data
    assert b'room-2' in response.data

def test_api_calculate_route(client):
    """Test the API calculate endpoint with valid JSON data."""
    test_data = {
        'room1': {'length': '10', 'width': '12', 'height': '8'},
        'room2': {'length': '15', 'width': '10', 'height': '9'}
    }
    response = client.post('/api/v1/calculate', 
                         data=json.dumps(test_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'room1' in data
    assert 'room2' in data
    assert 'total_gallons' in data
    assert isinstance(data['room1']['ft'], int)
    assert isinstance(data['room1']['gallons'], int)
    assert data['room1']['room'] == '1'  # Check room number extraction
    assert data['total_gallons'] >= 0  # Total gallons should be non-negative
