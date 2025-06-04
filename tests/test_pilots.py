import pytest
from unittest.mock import patch, MagicMock
from pilots import Pilots

@pytest.fixture
def pilots_instance():
    pilots = Pilots("test.db")
    pilots.db_ops = MagicMock()
    return pilots

def test_assign_pilot_to_flight_valid(monkeypatch, pilots_instance):
    # Mock input for flight_id and pilot_id
    inputs = iter(["12", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    pilots_instance.db_ops.execute_query = MagicMock()
    
    pilots_instance.assign_pilot_to_flight()
    
    pilots_instance.db_ops.execute_query.assert_called_once_with(
        """
        INSERT INTO flight_pilot (flight_number, pilot_id)
        VALUES (?, ?);
        """,
        ("12", "5")
    )

def test_assign_pilot_to_flight_invalid(monkeypatch, pilots_instance, capsys):
    # Non-numeric input for flight_id
    inputs = iter(["abc", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    pilots_instance.db_ops.execute_query = MagicMock()
    
    pilots_instance.assign_pilot_to_flight()
    captured = capsys.readouterr()
    assert "Invalid Flight Number" in captured.out
    pilots_instance.db_ops.execute_query.assert_not_called()