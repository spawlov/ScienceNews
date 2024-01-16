from django.test import TestCase
from requests import request

from ..utils import get_filename


class UtilsTest(TestCase):

    def test_get_filename(self):
        test_filename = ' TeSt FIle-namE .txt'
        result = get_filename(test_filename, request)
        self.assertEqual(result, '_test_file_name_.txt')

