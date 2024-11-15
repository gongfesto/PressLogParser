from src.log_parser import LogParser
import unittest

class TestLogParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = LogParser("")

    def test_parse_time_days_hours_minutes_seconds_ms(self):
        time_str = "T#1d19h56m1s172ms"
        expected_ms = (1 * 24 * 60 * 60 * 1000) + (19 * 60 * 60 * 1000) + (56 * 60 * 1000) + (1 * 1000) + 172
        self.assertEqual(self.parser.parse_time(time_str), expected_ms)

    def test_parse_time_minutes_seconds_ms(self):
        time_str = "T#4m17s47ms"
        expected_ms = (4 * 60 * 1000) + (17 * 1000) + 47
        self.assertEqual(self.parser.parse_time(time_str), expected_ms)

    def test_parse_time_hours_minutes_seconds_ms(self):
        time_str = "T#5h10m5s300ms"
        expected_ms = (5 * 60 * 60 * 1000) + (10 * 60 * 1000) + (5 * 1000) + 300
        self.assertEqual(self.parser.parse_time(time_str), expected_ms)

    def test_parse_time_only_ms(self):
        time_str = "T#500ms"
        expected_ms = 500
        self.assertEqual(self.parser.parse_time(time_str), expected_ms)

    def test_parse_time_only_seconds_ms(self):
        time_str = "T#15s250ms"
        expected_ms = (15 * 1000) + 250
        self.assertEqual(self.parser.parse_time(time_str), expected_ms)

if __name__ == "__main__":
    unittest.main()
