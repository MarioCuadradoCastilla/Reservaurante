import unittest
from unittest.mock import MagicMock, patch
from tkinter import TclError
from Controllers.BasicController import BasicController

class TestCancelAllEvents(unittest.TestCase):
    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_window.tk.call.return_value = ()
        self.mock_window.after_cancel = MagicMock()

    def test_cancel_all_events_no_events(self):
        BasicController.cancel_all_events(self.mock_window)
        self.mock_window.tk.call.assert_called_with('after', 'info')
        self.mock_window.after_cancel.assert_not_called()

    def test_cancel_all_events_with_events(self):
        self.mock_window.tk.call.return_value = ('event1', 'event2')
        BasicController.cancel_all_events(self.mock_window)
        self.mock_window.tk.call.assert_called_with('after', 'info')
        self.mock_window.after_cancel.assert_any_call('event1')
        self.mock_window.after_cancel.assert_any_call('event2')

    def test_cancel_all_events_invalid_command(self):
        self.mock_window.tk.call.return_value = ('event1',)
        self.mock_window.after_cancel.side_effect = TclError('invalid command name')
        BasicController.cancel_all_events(self.mock_window)
        self.mock_window.tk.call.assert_called_with('after', 'info')
        self.mock_window.after_cancel.assert_called_with('event1')

    @patch('builtins.print')
    def test_cancel_all_events_other_exception(self, mock_print):
        self.mock_window.tk.call.side_effect = Exception('Some error')
        BasicController.cancel_all_events(self.mock_window)
        mock_print.assert_called_with('Eventos que no pueden ser cancelados: Some error')

if __name__ == '__main__':
    unittest.main()



