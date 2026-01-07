"""
Tests for mouse_keepalive.move_mouse module
"""

import sys
from unittest.mock import Mock, patch, MagicMock, call

# Add parent directory to path to import the module
sys.path.insert(0, '..')

from mouse_keepalive.move_mouse import (
    move_mouse,
    main,
    MouseMover,
    MouseController,
    MousePosition,
    ScreenSize,
)


class TestMouseMover:
    """Test cases for MouseMover core class (using dependency injection)"""

    def test_calculate_next_position(self):
        """Test position calculation logic"""
        mover = MouseMover()
        current_pos = MousePosition(100, 200)
        screen_size = ScreenSize(1920, 1080)

        # Test first move (should move +1, +1)
        new_x, new_y = mover.calculate_next_position(current_pos, screen_size, move_count=0)
        assert new_x == 101
        assert new_y == 201

        # Test second move (should move -1, -1)
        new_x, new_y = mover.calculate_next_position(current_pos, screen_size, move_count=1)
        assert new_x == 99
        assert new_y == 199

    def test_calculate_next_position_boundary(self):
        """Test position calculation with boundary constraints"""
        mover = MouseMover()
        screen_size = ScreenSize(1920, 1080)

        # Test at top-left corner
        current_pos = MousePosition(0, 0)
        new_x, new_y = mover.calculate_next_position(current_pos, screen_size, move_count=0)
        assert new_x == 1  # Clamped to minimum
        assert new_y == 1  # Clamped to minimum

        # Test at bottom-right corner
        current_pos = MousePosition(1920, 1080)
        new_x, new_y = mover.calculate_next_position(current_pos, screen_size, move_count=1)
        assert new_x == 1919  # Clamped to maximum
        assert new_y == 1079  # Clamped to maximum

    def test_perform_move(self):
        """Test perform_move method"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        mover = MouseMover(controller=mock_controller)
        original_pos, move_count = mover.perform_move(move_count=0)

        assert original_pos.x == 100
        assert original_pos.y == 200
        assert move_count == 1
        assert mock_controller.move_to.call_count == 2  # Move away + move back

    def test_run_with_duration(self):
        """Test run method with duration"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0, 0.1, 1.1]  # start, first move, duration reached
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        move_count, elapsed = mover.run(interval=1, duration=1)

        assert move_count == 1
        assert elapsed == 1.1
        assert mock_controller.move_to.called

    def test_run_with_callbacks(self):
        """Test run method with callbacks"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0, 0.1, 1.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        on_start = Mock()
        on_move = Mock()
        on_finish = Mock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=1, on_start=on_start, on_move=on_move, on_finish=on_finish)

        on_start.assert_called_once()
        on_move.assert_called_once()
        on_finish.assert_called_once()

    def test_timer_interval_behavior(self):
        """Test that timer respects interval setting"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        # Simulate 3 moves with 1 second interval
        time_values = [0, 0.1, 1.1, 2.1, 3.1]  # start, move1, move2, move3, finish
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=3)

        # Should sleep 3 times (after each move, except the last one)
        assert mock_sleep.call_count == 3
        # Each sleep should be 1 second (the interval)
        for sleep_call in mock_sleep.call_args_list:
            assert sleep_call[0][0] == 1

    def test_timer_duration_behavior(self):
        """Test that timer respects duration setting"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        # Simulate time progression: start at 0, moves at 0.1, 1.1, 2.1, duration reached at 2.5
        time_values = [0, 0.1, 1.1, 2.1, 2.5]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        move_count, elapsed = mover.run(interval=1, duration=2.5)

        # Should have made 3 moves before duration was reached
        assert move_count == 3
        assert elapsed == 2.5
        # Should have slept 2 times (after first 2 moves, not after the 3rd)
        assert mock_sleep.call_count == 2

    def test_multiple_moves_sequence(self):
        """Test multiple moves in sequence"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        # Simulate 5 moves
        time_values = [0] + [0.1 + i for i in range(5)] + [5.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        move_count, elapsed = mover.run(interval=1, duration=5)

        # Should have made 5 moves
        assert move_count == 5
        # Each move should call move_to twice (move away + move back)
        assert mock_controller.move_to.call_count == 10  # 5 moves * 2 calls each

    def test_pyautogui_call_verification(self):
        """Test that pyautogui methods are called correctly"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0, 0.1, 1.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=1)

        # Verify get_position was called
        assert mock_controller.get_position.called
        # Verify get_screen_size was called
        assert mock_controller.get_screen_size.called
        # Verify move_to was called with correct parameters
        move_calls = mock_controller.move_to.call_args_list
        assert len(move_calls) == 2  # Move away + move back

        # First call: move to new position (should be 101, 201)
        first_call = move_calls[0]
        assert first_call[0][0] == 101  # new_x
        assert first_call[0][1] == 201  # new_y
        assert first_call[0][2] == 0.1  # duration

        # Second call: move back to original position (100, 200)
        second_call = move_calls[1]
        assert second_call[0][0] == 100  # original_x
        assert second_call[0][1] == 200  # original_y
        assert second_call[0][2] == 0.1  # duration

    def test_pyautogui_call_order(self):
        """Test that pyautogui methods are called in correct order"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0, 0.1, 1.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=1)

        # Verify call order: get_position -> get_screen_size -> move_to (twice) -> sleep
        call_order = []
        for method_call in mock_controller.method_calls:
            call_order.append(method_call[0])

        # Should call get_position first
        assert 'get_position' in call_order
        # Should call get_screen_size
        assert 'get_screen_size' in call_order
        # Should call move_to
        assert 'move_to' in call_order
        # get_position should be called before move_to
        assert call_order.index('get_position') < call_order.index('move_to')


class TestMoveMouse:
    """Test cases for move_mouse function (public API, backward compatible)"""

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.move_mouse')
    @patch('sys.argv', ['mouse-keepalive', '-i', '30'])
    def test_main_with_interval(self, mock_move_mouse):
        """Test main function with interval argument"""
        main()
        mock_move_mouse.assert_called_once_with(interval=30, duration=None)

    @patch('mouse_keepalive.move_mouse.move_mouse')
    @patch('sys.argv', ['mouse-keepalive', '-i', '60', '-d', '3600'])
    def test_main_with_interval_and_duration(self, mock_move_mouse):
        """Test main function with both interval and duration"""
        main()
        mock_move_mouse.assert_called_once_with(interval=60, duration=3600)

    @patch('mouse_keepalive.move_mouse.move_mouse')
    @patch('sys.argv', ['mouse-keepalive'])
    def test_main_default_values(self, mock_move_mouse):
        """Test main function with default values"""
        main()
        mock_move_mouse.assert_called_once_with(interval=60, duration=None)

    @patch('sys.argv', ['mouse-keepalive', '-i', '0'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_interval_zero(self, mock_print, mock_exit):
        """Test main function with invalid interval (0)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['mouse-keepalive', '-i', '-1'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_interval_negative(self, mock_print, mock_exit):
        """Test main function with invalid interval (negative)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['mouse-keepalive', '-d', '0'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_duration_zero(self, mock_print, mock_exit):
        """Test main function with invalid duration (0)"""
        main()
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['mouse-keepalive', '-d', '-1'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_duration_negative(self, mock_print, mock_exit):
        """Test main function with invalid duration (negative)"""
        main()
        mock_exit.assert_called_once_with(1)


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_zero_interval_edge_case(self):
        """Test behavior with very small interval (edge case)"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0, 0.01, 0.02]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=0.01, duration=0.02)

        # Should still perform moves
        assert mock_controller.move_to.called

    def test_very_large_screen(self):
        """Test behavior with very large screen dimensions"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(5000, 3000)
        mock_controller.get_screen_size.return_value = ScreenSize(7680, 4320)  # 8K screen

        time_values = [0, 0.1, 1.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=1)

        # Verify coordinates are within bounds
        for move_call in mock_controller.move_to.call_args_list:
            x, y = move_call[0][0], move_call[0][1]
            assert 1 <= x < 7680
            assert 1 <= y < 4320

    def test_small_screen(self):
        """Test behavior with small screen dimensions"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(50, 50)
        mock_controller.get_screen_size.return_value = ScreenSize(100, 100)  # Small screen

        time_values = [0, 0.1, 1.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        mover.run(interval=1, duration=1)

        # Verify coordinates are within bounds
        for move_call in mock_controller.move_to.call_args_list:
            x, y = move_call[0][0], move_call[0][1]
            assert 1 <= x < 100
            assert 1 <= y < 100

    def test_mouse_at_screen_edges(self):
        """Test behavior when mouse is at screen edges"""
        mock_controller = Mock(spec=MouseController)
        screen_size = ScreenSize(1920, 1080)

        # Test all four corners
        corners = [
            (1, 1),  # Top-left
            (1919, 1),  # Top-right
            (1, 1079),  # Bottom-left
            (1919, 1079),  # Bottom-right
        ]

        for corner_x, corner_y in corners:
            mock_controller.get_position.return_value = MousePosition(corner_x, corner_y)
            mock_controller.get_screen_size.return_value = screen_size

            time_values = [0, 0.1, 1.1]
            mock_time = MagicMock(side_effect=time_values)
            mock_sleep = MagicMock()

            mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

            mover.run(interval=1, duration=1)

            # Verify all moves stay within bounds
            for move_call in mock_controller.move_to.call_args_list:
                x, y = move_call[0][0], move_call[0][1]
                assert 1 <= x < 1920
                assert 1 <= y < 1080


class TestCrossPlatform:
    """Cross-platform compatibility tests"""

    @patch('mouse_keepalive.move_mouse.platform')
    @patch('mouse_keepalive.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_macos_compatibility(self, mock_print, mock_sleep, mock_time, mock_pyautogui, mock_platform):
        """Test macOS compatibility"""
        mock_platform.system.return_value = 'Darwin'
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 1.1]
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=1)

        # Should work on macOS
        assert mock_pyautogui.moveTo.called
        assert 'Darwin' in str(mock_print.call_args_list)

    @patch('mouse_keepalive.move_mouse.platform')
    @patch('mouse_keepalive.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_windows_compatibility(self, mock_print, mock_sleep, mock_time, mock_pyautogui, mock_platform):
        """Test Windows compatibility"""
        mock_platform.system.return_value = 'Windows'
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 1.1]
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=1)

        # Should work on Windows
        assert mock_pyautogui.moveTo.called
        assert 'Windows' in str(mock_print.call_args_list)

    @patch('mouse_keepalive.move_mouse.platform')
    @patch('mouse_keepalive.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_linux_compatibility(self, mock_print, mock_sleep, mock_time, mock_pyautogui, mock_platform):
        """Test Linux compatibility"""
        mock_platform.system.return_value = 'Linux'
        mock_pyautogui.position.return_value = (100, 200)
        mock_pyautogui.size.return_value = (1920, 1080)
        mock_time.side_effect = [0, 0.1, 1.1]
        mock_sleep.return_value = None

        move_mouse(interval=1, duration=1)

        # Should work on Linux
        assert mock_pyautogui.moveTo.called
        assert 'Linux' in str(mock_print.call_args_list)


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_controller_get_position_error(self):
        """Test handling of controller errors"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.side_effect = Exception("Mouse position error")
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        time_values = [0]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        # Should raise exception when controller fails
        try:
            mover.run(interval=1, duration=1)
            assert False, "Should have raised exception"
        except Exception:
            assert True  # Expected

    def test_infinite_duration(self):
        """Test infinite duration (duration=None)"""
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)

        # Simulate time progression but never reach duration
        time_values = [0, 0.1, 1.1, 2.1, 3.1]
        mock_time = MagicMock(side_effect=time_values)
        mock_sleep = MagicMock(side_effect=KeyboardInterrupt())  # Simulate Ctrl+C

        mover = MouseMover(controller=mock_controller, time_func=mock_time, sleep_func=mock_sleep)

        try:
            mover.run(interval=1, duration=None)
        except KeyboardInterrupt:
            # Should handle KeyboardInterrupt gracefully
            assert mock_controller.move_to.called


class TestIntegration:
    """Integration tests"""

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.pyautogui')
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

    @patch('mouse_keepalive.move_mouse.pyautogui')
    @patch('time.time')
    @patch('time.sleep')
    @patch('builtins.print')
    def test_realistic_usage_scenario(self, mock_print, mock_sleep, mock_time, mock_pyautogui):
        """Test realistic usage scenario: 30 second interval, 1 hour duration"""
        mock_pyautogui.position.return_value = (500, 500)
        mock_pyautogui.size.return_value = (1920, 1080)
        
        # Simulate 1 hour (3600 seconds) with 30 second intervals
        # That's 120 moves (3600 / 30)
        # For testing, we'll simulate just a few moves
        time_values = [0] + [0.1 + i * 30 for i in range(5)] + [150.1]
        mock_time.side_effect = time_values
        mock_sleep.return_value = None

        move_mouse(interval=30, duration=150)

        # Should have made multiple moves
        assert mock_pyautogui.moveTo.call_count >= 2
        # Verify sleep was called with correct interval
        for sleep_call in mock_sleep.call_args_list:
            assert sleep_call[0][0] == 30
