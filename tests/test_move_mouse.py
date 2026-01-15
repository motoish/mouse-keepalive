"""
Tests for mouse_keepalive.move_mouse module
"""

import sys
from pathlib import Path
import pytest
from unittest.mock import Mock, patch, MagicMock

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mouse_keepalive.move_mouse import (
    MouseMover,
    MouseController,
    MousePosition,
    ScreenSize,
    move_mouse,
    main,
)

# Get the module object from sys.modules for patching
move_mouse_module = sys.modules['mouse_keepalive.move_mouse']


class TestMouseMoverCore:
    def test_calculate_next_position(self):
        mover = MouseMover()
        screen = ScreenSize(1920, 1080)

        assert mover.calculate_next_position(MousePosition(100, 200), screen, 0) == (101, 201)
        assert mover.calculate_next_position(MousePosition(100, 200), screen, 1) == (99, 199)

        x, y = mover.calculate_next_position(MousePosition(0, 0), screen, 0)
        assert (x, y) == (1, 1)

        x, y = mover.calculate_next_position(MousePosition(1920, 1080), screen, 1)
        assert (x, y) == (1919, 1079)

    def test_perform_move_calls_controller(self):
        ctrl = Mock(spec=MouseController)
        ctrl.get_position.return_value = MousePosition(100, 200)
        ctrl.get_screen_size.return_value = ScreenSize(1920, 1080)

        mover = MouseMover(controller=ctrl)
        original, next_count, success = mover.perform_move(move_count=0)

        assert original == MousePosition(100, 200)
        assert next_count == 1
        assert success is True
        assert ctrl.move_to.call_count == 2

    def test_run_interval_and_duration(self):
        ctrl = Mock(spec=MouseController)
        ctrl.get_position.return_value = MousePosition(100, 200)
        ctrl.get_screen_size.return_value = ScreenSize(1920, 1080)

        times = [0, 0.1, 1.1, 2.1, 2.1]
        mock_time = MagicMock(side_effect=times)
        mock_sleep = MagicMock()

        mover = MouseMover(controller=ctrl, time_func=mock_time, sleep_func=mock_sleep)
        move_count, elapsed = mover.run(interval=1, duration=2)

        assert move_count >= 2
        assert elapsed == 2.1
        assert mock_sleep.call_count >= 2

    def test_run_callbacks_are_called(self):
        ctrl = Mock(spec=MouseController)
        ctrl.get_position.return_value = MousePosition(100, 200)
        ctrl.get_screen_size.return_value = ScreenSize(1920, 1080)

        times = [0, 0.1, 1.1, 1.1]
        mock_time = MagicMock(side_effect=times)
        mock_sleep = MagicMock()

        on_start = Mock()
        on_move = Mock()
        on_finish = Mock()

        mover = MouseMover(controller=ctrl, time_func=mock_time, sleep_func=mock_sleep)
        mover.run(
            interval=1, duration=1,
            on_start=on_start, on_move=on_move, on_finish=on_finish
        )

        on_start.assert_called_once()
        assert on_move.call_count >= 1
        on_finish.assert_called_once()


class TestMoveMouseAPI:
    @patch.object(move_mouse_module, "MouseController")
    @patch("time.sleep")
    @patch("time.time")
    def test_move_mouse_basic(self, mock_time, mock_sleep, mock_controller_cls):
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)
        mock_controller_cls.return_value = mock_controller

        mock_time.side_effect = [0, 0.1, 1.1, 1.1]

        move_mouse(interval=1, duration=1)

        mock_controller.get_position.assert_called()
        mock_controller.move_to.assert_called()

    @patch.object(move_mouse_module, "MouseController")
    @patch("time.sleep")
    @patch("time.time")
    def test_move_mouse_bounds(self, mock_time, mock_sleep, mock_controller_cls):
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(0, 0)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)
        mock_controller_cls.return_value = mock_controller

        mock_time.side_effect = [0, 0.1, 1.1, 1.1]

        move_mouse(interval=1, duration=1)

        # Check that move_to was called with valid coordinates
        # First call should be to new position (clamped to bounds), second back to original
        move_calls = mock_controller.move_to.call_args_list
        assert len(move_calls) >= 2
        
        # First call: move to new position (should be clamped to 1, 1)
        first_call = move_calls[0]
        x1, y1 = first_call.args[0], first_call.args[1]
        assert 1 <= x1 < 1920
        assert 1 <= y1 < 1080
        
        # Second call: move back to original position (0, 0) - this is expected
        # The bounds check ensures the new position is valid, not the original

    @patch.object(move_mouse_module, "MouseController")
    @patch("time.sleep", side_effect=KeyboardInterrupt())
    @patch("time.time")
    def test_interrupt_does_not_crash(self, mock_time, mock_sleep, mock_controller_cls):
        mock_controller = Mock(spec=MouseController)
        mock_controller.get_position.return_value = MousePosition(100, 200)
        mock_controller.get_screen_size.return_value = ScreenSize(1920, 1080)
        mock_controller_cls.return_value = mock_controller

        mock_time.side_effect = [0, 0.1, 0.1]
        move_mouse(interval=1, duration=None)


class TestMainCLI:
    @patch.object(move_mouse_module, "move_mouse")
    def test_main_with_interval(self, mock_move):
        import sys
        orig = sys.argv
        sys.argv = ["mouse-keepalive", "-i", "30"]
        try:
            main()
        finally:
            sys.argv = orig

        mock_move.assert_called_once_with(interval=30, duration=None, verbose=False)

    @patch.object(move_mouse_module, "move_mouse")
    @patch("builtins.print")
    def test_main_invalid_params_exit(self, mock_print, mock_move_mouse):
        """Test that main() handles invalid parameters correctly"""
        import sys
        orig_argv = sys.argv
        
        for argv in [
            ["mouse-keepalive", "-i", "0"],
            ["mouse-keepalive", "-i", "-5"],
            ["mouse-keepalive", "-d", "0"],
        ]:
            sys.argv = argv
            # sys.exit will be called, which raises SystemExit
            # pytest may handle this, so we just verify error message was printed
            try:
                main()
            except SystemExit:
                pass  # Expected - sys.exit raises SystemExit
            
            # Verify error message was printed
            print_messages = []
            for call in mock_print.call_args_list:
                if call.args:
                    print_messages.append(str(call.args[0]))
            
            assert any("错误" in msg or "Error" in msg for msg in print_messages), \
                f"Expected error message for argv {argv}, got: {print_messages}"
            
            # move_mouse should not be called for invalid params
            # (even if sys.exit doesn't work, we've mocked move_mouse to prevent infinite loops)
            mock_move_mouse.assert_not_called()
            
            mock_print.reset_mock()
            mock_move_mouse.reset_mock()
        
        sys.argv = orig_argv
