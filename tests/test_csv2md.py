import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from csv2md import convert

SCRIPT = os.path.join(ROOT, "csv2md.py")


def run(args, stdin=b""):
    return subprocess.run([sys.executable, SCRIPT] + args, input=stdin, capture_output=True)


class ConvertTests(unittest.TestCase):
    def test_simple_table(self):
        self.assertEqual(convert("a,b\n1,2\n"), "| a | b |\n| --- | --- |\n| 1 | 2 |\n")

    def test_quoted_comma(self):
        self.assertEqual(convert('name\n"Smith, J"\n'), "| name |\n| --- |\n| Smith, J |\n")

    def test_quoted_newline(self):
        self.assertEqual(convert('a\n"line1\nline2"\n'), "| a |\n| --- |\n| line1<br>line2 |\n")

    def test_quoted_crlf(self):
        self.assertEqual(convert('a\r\n"x\r\ny"\r\n'), "| a |\n| --- |\n| x<br>y |\n")

    def test_doubled_quotes(self):
        self.assertEqual(convert('a\n"say ""hi"""\n'), '| a |\n| --- |\n| say "hi" |\n')

    def test_pipe_escaped(self):
        self.assertEqual(convert("a\nx|y\n"), "| a |\n| --- |\n| x\\|y |\n")

    def test_empty_cells(self):
        self.assertEqual(convert("a,b,c\n,2,\n"), "| a | b | c |\n| --- | --- | --- |\n|  | 2 |  |\n")

    def test_data_row_longer_than_header(self):
        self.assertEqual(convert("a\n1,2\n"), "| a |  |\n| --- | --- |\n| 1 | 2 |\n")

    def test_data_row_shorter(self):
        self.assertEqual(convert("a,b,c\n1\n"), "| a | b | c |\n| --- | --- | --- |\n| 1 |  |  |\n")

    def test_bom_stripped(self):
        self.assertEqual(convert("﻿a,b\n1,2\n"), "| a | b |\n| --- | --- |\n| 1 | 2 |\n")

    def test_non_ascii(self):
        self.assertEqual(convert("city,café\nZürich,東京\n"), "| city | café |\n| --- | --- |\n| Zürich | 東京 |\n")

    def test_whitespace_stripped(self):
        self.assertEqual(convert(" a , b \n 1 ,2\n"), "| a | b |\n| --- | --- |\n| 1 | 2 |\n")

    def test_blank_input(self):
        self.assertEqual(convert(""), "")

    def test_delimiter(self):
        self.assertEqual(convert("a;b\n1;2\n", delimiter=";"), "| a | b |\n| --- | --- |\n| 1 | 2 |\n")


class CliTests(unittest.TestCase):
    EXPECTED = b"| a | b |\n| --- | --- |\n| 1 | 2 |\n"

    def test_file_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "in.csv")
            with open(path, "wb") as handle:
                handle.write(b"\xef\xbb\xbfa,b\n1,2\n")
            result = run([path])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.EXPECTED)

    def test_stdin_no_argument(self):
        result = run([], b"a,b\n1,2\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.EXPECTED)

    def test_stdin_dash(self):
        result = run(["-"], b"a,b\n1,2\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.EXPECTED)

    def test_blank_input(self):
        result = run([], b"")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")

    def test_missing_file(self):
        result = run([os.path.join(ROOT, "does-not-exist.csv")])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, b"")
        self.assertNotEqual(result.stderr.strip(), b"")

    def test_delimiter_flag(self):
        result = run(["--delimiter", ";"], b"a;b\n1;2\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.EXPECTED)


if __name__ == "__main__":
    unittest.main()
