import unittest
from unittest.mock import MagicMock, patch
from tkinter import TclError
import os
from Controllers.BasicController import BasicController

class TestBasicController(unittest.TestCase):
    def setUp(self):
        self.mock_window = MagicMock()
        self.mock_widget = MagicMock()
        self.mock_window.tk.eval.return_value = ''
        self.mock_window.after_cancel = MagicMock()

    def test_cancel_after_scripts_no_events(self):
        BasicController.cancel_after_scripts(self.mock_window)
        self.mock_window.tk.eval.assert_called_with('after info')
        self.mock_window.after_cancel.assert_not_called()

    def test_cancel_after_scripts_with_events(self):
        self.mock_window.tk.eval.return_value = 'event1 event2'
        BasicController.cancel_after_scripts(self.mock_window)
        self.mock_window.tk.eval.assert_called_with('after info')
        self.mock_window.after_cancel.assert_any_call('event1')
        self.mock_window.after_cancel.assert_any_call('event2')

    def test_cancel_after_scripts_invalid_command(self):
        self.mock_window.tk.eval.return_value = 'event1'
        self.mock_window.after_cancel.side_effect = TclError('invalid command name')
        BasicController.cancel_after_scripts(self.mock_window)
        self.mock_window.tk.eval.assert_called_with('after info')
        self.mock_window.after_cancel.assert_called_with('event1')

    @patch('builtins.print')
    def test_cancel_after_scripts_other_exception(self, mock_print):
        self.mock_window.tk.eval.side_effect = Exception('Some error')
        BasicController.cancel_after_scripts(self.mock_window)
        mock_print.assert_called_with('Eventos que no pueden ser cancelados: Some error')

    def test_unbind_all_events(self):
        BasicController.unbind_all_events(self.mock_widget)
        self.mock_widget.unbind.assert_any_call("<Button-1>")
        self.mock_widget.unbind.assert_any_call("<Enter>")
        self.mock_widget.unbind.assert_any_call("<Leave>")

    def test_complete_destruction_and_transition(self):
        callback = MagicMock()
        BasicController.complete_destruction_and_transition(self.mock_window, callback)
        self.mock_window.destroy.assert_called_once()
        callback.assert_called_once()

    @patch('os.path.dirname')
    @patch('os.path.abspath')
    @patch('builtins.open')
    @patch('json.load')
    def test_load_municipalities(self, mock_json_load, mock_open, mock_abspath, mock_dirname):
        mock_abspath.return_value = '/mock/path'
        mock_dirname.return_value = '/mock'
        mock_json_load.return_value = {'municipios': ['Municipio1', 'Municipio2']}

        # Use os.path.join for consistent path representation
        expected_path = os.path.join('/mock', '..', 'Data', 'Municipality', 'Municipalities.json')

        result = BasicController.load_municipalities()
        mock_open.assert_called_with(expected_path, 'r', encoding='utf-8')
        self.assertEqual(result, ['Municipio1', 'Municipio2'])


if __name__ == '__main__':
    unittest.main()



