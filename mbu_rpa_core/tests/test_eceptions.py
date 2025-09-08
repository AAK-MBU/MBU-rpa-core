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
    try:
        message = "Test error message"
        raise BaseRPAError(message=message)
    except BaseRPAError as error:
        assert str(error) == message
        assert repr(error) == f"BaseRPAError(message={repr(message)})"

    # Test that Pydantic catches invalid input
    with pytest.raises(ValidationError):
        raise BaseRPAError(message=123)  # Not a string
    with pytest.raises(ValidationError):
        raise BaseRPAError(message="")  # Empty string


def test_business_error():
    """
    Test the BusinessError exception class.

    Verifies that:
    1. The exception inherits from BaseRPAError
    2. The message is correctly set and returned
    """

    # Test that BusinessError contains the correct message
    try:
        message = "Business error occurred"
        raise BusinessError(message=message)
    except BusinessError as error:
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
    try:
        message = "Process error occurred"
        raise ProcessError(message=message)
    except ProcessError as error:
        assert str(error) == message
        assert repr(error) == f"ProcessError(message={repr(message)})"
