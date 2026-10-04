import unittest

from gary.host import command_exists, read_os_release


class HostTests(unittest.TestCase):
    def test_read_os_release_shape(self):
        data = read_os_release()
        self.assertIsInstance(data, dict)
        if data:
            self.assertIn("ID", data)

    def test_python_exists(self):
        self.assertTrue(command_exists("python3"))
