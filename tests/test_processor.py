import unittest
from processor import text_replace

class TestTextReplace(unittest.TestCase):
    def test_text_replace(self):
        input_text = """hello world
this is a foo test
goodbye foo"""

        expected_output = """hi world
this is a bar test
goodbye bar"""

        rules = [
            {"search": "foo", "replace": "bar"},
            {"search": "hello", "replace": "hi"}
        ]

        updated_text, results = text_replace(input_text, rules)

        self.assertEqual(updated_text, expected_output)
        self.assertTrue(all("search_text" in result and "replace_text" in result for result in results))


if __name__ == "__main__":
    unittest.main()
