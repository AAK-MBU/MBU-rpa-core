"""
Unit tests for process completion states in the MBU RPA Core library.

This module contains tests for the Pydantic models and enums defined in process_states.py.
The tests verify that process states are properly initialized with messages and that
Pydantic validation works as expected for invalid input.
"""

import pytest
from pydantic import ValidationError
from mbu_rpa_core.process_states import CompletedState, StateType


def test_state_type_enum():
    """
    Test the StateType enumeration.

    Verifies that:
    1. The enum has the correct members
    2. The auto() values are properly assigned
    """
    # Test that enum members exist
    assert StateType.COMPLETED in StateType
    assert StateType.COMPLETED_WITH_EXCEPTION in StateType

    # Test that auto() values are unique
    assert StateType.COMPLETED.value != StateType.COMPLETED_WITH_EXCEPTION.value


def test_factory_methods():
    """
    Test the CompletedState model initialization.

    Verifies that:
    1. The model is properly initialized with state and message
    2. The __str__ method returns the correct string representation
    """
    # Test completed factory method
    message = "Process completed successfully"
    state = CompletedState.completed(message=message)

    assert state.state == StateType.COMPLETED
    assert state.message == message
    assert str(state) == f"Completed: {message}"

    class_state = CompletedState(state=StateType.COMPLETED, message=message)

    assert class_state == state

    # Test completed_with_exception factory method
    exception_message = "Process completed with an exception"
    exception_state = CompletedState.completed_with_exception(exception_message)

    assert exception_state.state == StateType.COMPLETED_WITH_EXCEPTION
    assert exception_state.message == exception_message
    assert str(exception_state) == f"Completed with exceptions: {exception_message}"

    exception_class_state = CompletedState(state=StateType.COMPLETED_WITH_EXCEPTION, message=exception_message)

    assert exception_class_state == exception_state


def test_completed_state_validation():
    """
    Test the CompletedState model validation.

    Verifies that:
    1. Pydantic raises ValidationError for invalid input
    2. The message validator works correctly
    """
    # Test that Pydantic catches invalid input
    with pytest.raises(ValidationError):
        CompletedState(state=StateType.COMPLETED, message=123)  # Not a string

    with pytest.raises(ValidationError):
        CompletedState(state=StateType.COMPLETED, message="")  # Empty string

    # Test that factory methods validate their input
    with pytest.raises(ValidationError):
        CompletedState.completed("")  # Empty string

    with pytest.raises(ValidationError):
        CompletedState.completed_with_exception(123)  # Not a string
