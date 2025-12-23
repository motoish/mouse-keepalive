"""
Pytest configuration and fixtures
"""

import sys
from unittest.mock import MagicMock

# Mock pyautogui before any imports
mock_pyautogui = MagicMock()
mock_pyautogui.FAILSAFE = False
sys.modules['pyautogui'] = mock_pyautogui

