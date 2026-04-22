# mbu_dev_shared_components/database/__init__.py
"""Database module exposing core connection utilities.

This module provides access to the main database connection class
used throughout the application.
"""

from .connection import RPAConnection

__all__ = ["RPAConnection"]
