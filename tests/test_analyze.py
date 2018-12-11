import unittest
from cli.doppel.bin.analyze.py as al


class AnalyzeTest(unittest.TestCase):
    
   	#Test for _log_info and should print msg
	def test_log_info(self):

		self.assertEqual(al._log_info("Hello World!"), "Hello World", "Printed the msg")


	#Test for _get_arg_names and should return arg names.
	#def test_get_arg_names(self):

		#self.assertEqual(al._get_arg_names(), )
