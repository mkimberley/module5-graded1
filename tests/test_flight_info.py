import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import tabulate
from flight_info import FlightInfo

@pytest.fixture
def mock_db_ops(mocker):
    """Fixture to mock DBOperations."""
    mock_db_ops = mocker.MagicMock()
    return mock_db_ops

@pytest.fixture
def flight_info(mock_db_ops):
    """Fixture to create a FlightInfo instance with mocked DBOperations."""
    flight_info = FlightInfo("test.db")
    flight_info.db_ops = mock_db_ops
    return flight_info

def test_create_flight_validations(mocker, flight_info, mock_db_ops):
    # Arrange
    mocker.patch('builtins.input', side_effect=[
        "FL123",  # flight_number
        "DEP001",  # departure_airport_id
        "ARR001",  # arrival_airport_id
        "2025-06-03 10:00:00",  # departure_time
        "2025-06-03 14:00:00",  # arrival_time
        "AC001",  # aircraft_id
        "Scheduled"  # status
    ])
    mock_db_ops.validate_fields.return_value = True
    mock_db_ops.execute_query.return_value = None

    # Act
    flight_info.create_flight()

    # Assert
    validations = [
        {"table": "airports", "column": "airport_id", "value": "DEP001", "validation_type": "existing"},
        {"table": "airports", "column": "airport_id", "value": "ARR001", "validation_type": "existing"},
        {"table": "aircraft", "column": "aircraft_id", "value": "AC001", "validation_type": "existing"},
        {"table": "flights", "column": "flight_number", "value": "FL123", "validation_type": "unique"},
    ]
    mock_db_ops.validate_fields.assert_called_once_with(validations)
    mock_db_ops.execute_query.assert_called_once()

def test_create_flight_invalid_airport(mocker, flight_info, mock_db_ops):
    # Arrange
    mocker.patch('builtins.input', side_effect=[
        "FL123",  # flight_number
        "DEP001",  # departure_airport_id
        "ARR001",  # arrival_airport_id
        "2025-06-03 10:00:00",  # departure_time
        "2025-06-03 14:00:00",  # arrival_time
        "AC001",  # aircraft_id
        "Scheduled"  # status
    ])
    mock_db_ops.validate_fields.side_effect = ValueError("Invalid airport ID")

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid airport ID"):
        flight_info.create_flight()
    mock_db_ops.validate_fields.assert_called()

def test_create_flight_duplicate_flight_number(mocker, flight_info, mock_db_ops):
    # Arrange
    mocker.patch('builtins.input', side_effect=[
        "FL123",  # flight_number
        "DEP001",  # departure_airport_id
        "ARR001",  # arrival_airport_id
        "2025-06-03 10:00:00",  # departure_time
        "2025-06-03 14:00:00",  # arrival_time
        "AC001",  # aircraft_id
        "Scheduled"  # status
    ])
    mock_db_ops.validate_fields.side_effect = ValueError("Flight number already exists")

    # Act & Assert
    with pytest.raises(ValueError, match="Flight number already exists"):
        flight_info.create_flight()
    mock_db_ops.validate_fields.assert_called()