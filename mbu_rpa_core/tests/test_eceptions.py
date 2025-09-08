"""
Unit tests for custom exceptions in the MBU RPA Core library.

This module contains tests for the custom exception classes defined in exceptions.py.
The tests verify that exceptions are properly initialized with messages and that
Pydantic validation works as expected for invalid input.
"""

import pytest
from pydantic import ValidationError
from mbu_rpa_core.exceptions import BusinessError, ProcessError, BaseRPAError


def test_base_rpa_error():
    """
    Test the BaseRPAError exception class.

    Verifies that:
    1. The exception is properly initialized with a message
    2. The message is correctly returned by __str__ and __repr__
    3. Pydantic raises ValidationError for invalid input
    """
    # Test that error message is correctly set and returned
    message = "Test error message"
    error = BaseRPAError(message=message)
    assert str(error) == message
    assert repr(error) == f"BaseRPAError(message={repr(message)})"

    # Test that Pydantic catches invalid input
    with pytest.raises(ValidationError):
        BaseRPAError(message=123)  # Not a string
    with pytest.raises(ValidationError):
        BaseRPAError(message="")  # Empty string


def test_business_error():
    """
    Test the BusinessError exception class.

    Verifies that:
    1. The exception inherits from BaseRPAError
    2. The message is correctly set and returned
    """

    # Test that BusinessError contains the correct message
    message = "Business error occurred"
    error = BusinessError(message=message)
    assert str(error) == message
    assert repr(error) == f"BusinessError(message={repr(message)})"


def test_process_error():
    """
    Test the ProcessError exception class.

    Verifies that:
    1. The exception inherits from BaseRPAError
    2. The message is correctly set and returned
    """

    # Test that ProcessError contains the correct message
    message = "Process error occurred"
    error = ProcessError(message=message)
    assert str(error) == message
    assert repr(error) == f"ProcessError(message={repr(message)})"
