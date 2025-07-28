import unittest
from arg_parser import parse_args


class TestArgParser(unittest.TestCase):
    def test_arg_parser(self):
        args = parse_args([
            '--days', '13'
        ])
        self.assertEqual(args.days, 13)
