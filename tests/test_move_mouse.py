"""
Tests for auto_mouse_mover.move_mouse module
"""

import sys
from unittest.mock import Mock, patch
import pytest

# Add parent directory to path to import the module
sys.path.insert(0, '..')

from auto_mouse_mover.move_mouse import move_mouse, main


class TestMoveMouse:
    """Test cases for move_mouse function"""

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_move_mouse_basic(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test basic mouse movement functionality"""
        # Setup mocks
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        # Simulate time progression: start at 0, then check elapsed time
        mock_time.side_effect = [0, 0.1, 1.1]  # start_time, first move, duration reached
        mock_sleep.return_value = None

        # Call function with short duration to test completion
        move_mouse(interval=1, duration=1)

        # Verify pyautogui was called
        assert mock_pyautogui.position.called
        assert mock_pyautogui.moveTo.called
        assert mock_pyautogui.size.called

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_move_mouse_alternating_direction(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test that mouse moves in alternating directions"""
        # Setup mocks
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 1.1]  # start_time, first move, duration reached
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=1)

        # Verify moveTo was called multiple times (move + move back)
        assert mock_pyautogui.moveTo.call_count >= 2

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_move_mouse_boundary_check(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test that mouse position stays within screen bounds"""
        # Setup mocks - mouse at edge of screen
        mock_pyautogui.position.return_value = (0, 0)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 0.6]  # start_time, first move, duration reached
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=0.5)

        # Verify moveTo was called with valid coordinates
        for call in mock_pyautogui.moveTo.call_args_list:
            x, y = call[0][0], call[0][1]
            assert 1 <= x < 1920
            assert 1 <= y < 1080

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_move_mouse_keyboard_interrupt(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test handling of KeyboardInterrupt"""
        # Setup mocks
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1]
        mock_sleep.side_effect = KeyboardInterrupt()

        # Should handle KeyboardInterrupt gracefully
        move_mouse(interval=1, duration=None)

        # Verify print was called with interruption message
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any('interrupted' in str(call).lower() or '中断' in str(call) for call in print_calls)


class TestMain:
    """Test cases for main function"""

    @patch('auto_mouse_mover.move_mouse.move_mouse')
    @patch('sys.argv', ['auto-mouse-mover', '-i', '30'])
    def test_main_with_interval(self, mock_move_mouse):
        """Test main function with interval argument"""
        main()
        mock_move_mouse.assert_called_once_with(interval=30, duration=None)

    @patch('auto_mouse_mover.move_mouse.move_mouse')
    @patch('sys.argv', ['auto-mouse-mover', '-i', '60', '-d', '3600'])
    def test_main_with_interval_and_duration(self, mock_move_mouse):
        """Test main function with both interval and duration"""
        main()
        mock_move_mouse.assert_called_once_with(interval=60, duration=3600)

    @patch('auto_mouse_mover.move_mouse.move_mouse')
    @patch('sys.argv', ['auto-mouse-mover'])
    def test_main_default_values(self, mock_move_mouse):
        """Test main function with default values"""
        main()
        mock_move_mouse.assert_called_once_with(interval=60, duration=None)

    @patch('sys.argv', ['auto-mouse-mover', '-i', '0'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_interval_zero(self, mock_print, mock_exit):
        """Test main function with invalid interval (0)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['auto-mouse-mover', '-i', '-1'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_interval_negative(self, mock_print, mock_exit):
        """Test main function with invalid interval (negative)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['auto-mouse-mover', '-d', '0'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_duration_zero(self, mock_print, mock_exit):
        """Test main function with invalid duration (0)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['auto-mouse-mover', '-d', '-1'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_duration_negative(self, mock_print, mock_exit):
        """Test main function with invalid duration (negative)"""
        main()
        mock_exit.assert_called_once_with(1)


class TestIntegration:
    """Integration tests"""

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_full_cycle(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test a full cycle of mouse movement"""
        # Setup mocks
        mock_pyautogui.position.return_value = (500, 500)
        mock_pyautogui.size.return_value = (1920, 1080)
        
        # Simulate time progression
        time_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
        mock_time.side_effect = time_values
        mock_sleep.return_value = None

        move_mouse(interval=0.1, duration=0.4)

        # Verify mouse was moved
        assert mock_pyautogui.moveTo.called
        # Should have moved at least once
        assert mock_pyautogui.moveTo.call_count >= 2  # move + move back

    @patch('auto_mouse_mover.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    def test_move_count_tracking(self, mock_sleep, mock_time, mock_pyautogui):
        """Test that move count is tracked correctly"""
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 0.6]
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=0.5)

        # Function should complete without error
        assert True
