import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = """
Some regular text

# Introduction

More text here

## Subsection

# Another Main Section

More content
"""
        title = extract_title(md)
        expected = "Introduction"
        self.assertEqual(expected, title)

    def test_raise_error(self):
        md = """
Some regular text

More text here

## Subsection

More content
"""
        with self.assertRaises(ValueError) as context:
            extract_title(md)

        expected = "there is no h1 title"
        self.assertEqual(expected, str(context.exception))


if __name__ == '__main__':
    unittest.main()
