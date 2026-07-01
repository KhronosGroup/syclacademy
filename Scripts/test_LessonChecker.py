import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import LessonChecker


class TestSYCLAParser(unittest.TestCase):

    def setUp(self):
        self.parser = LessonChecker.SYCLAParser("Test Lesson", False, False)

    def tearDown(self) -> None:
        return super().tearDown()

    # ---------------------------------------------------------------------
    # Construction / defaults
    # ---------------------------------------------------------------------

    def test_initial_state(self):
        self.assertEqual(self.parser.code_blocks, [])
        self.assertEqual(self.parser.output, [])
        self.assertFalse(self.parser.is_code)
        self.assertFalse(self.parser.is_mark)
        self.assertFalse(self.parser.parser_error)
        self.assertEqual(self.parser.lesson_name, "Test Lesson")
        self.assertFalse(self.parser.extract)
        self.assertFalse(self.parser.verify)

    # ---------------------------------------------------------------------
    # handle_starttag
    # ---------------------------------------------------------------------

    def test_starttag_code_sets_flag_and_class(self):
        self.parser.handle_starttag("code", [])
        self.assertTrue(self.parser.is_code)
        self.assertEqual(self.parser.output[0], '<code class="language-cpp">')
        self.assertEqual(len(self.parser.code_blocks), 1)
        self.assertEqual(self.parser.code_blocks[0][1], "")

    def test_starttag_code_overwrites_existing_class(self):
        self.parser.handle_starttag("code", [("class", "something-else")])
        self.assertEqual(self.parser.output[0], '<code class="language-cpp">')

    def test_starttag_mark_sets_flag(self):
        self.parser.handle_starttag("mark", [])
        self.assertTrue(self.parser.is_mark)
        self.assertEqual(self.parser.output[0], "<mark>")

    def test_starttag_regular_tag_with_attrs(self):
        self.parser.handle_starttag("a", [("href", "foo"), ("disabled", None)])
        self.assertEqual(self.parser.output[0], '<a href="foo" disabled>')

    def test_starttag_attr_value_true(self):
        self.parser.handle_starttag("input", [("checked", True)])  # pyright: ignore
        self.assertEqual(self.parser.output[0], "<input checked>")

    def test_starttag_attr_value_stripped(self):
        self.parser.handle_starttag("a", [("href", "  foo  ")])
        self.assertEqual(self.parser.output[0], '<a href="foo">')

    def test_starttag_span_in_code_sets_error(self):
        self.parser.is_code = True
        self.parser.handle_starttag("span", [])
        self.assertTrue(self.parser.parser_error)
        # span is still emitted to output
        self.assertEqual(self.parser.output[0], "<span>")

    def test_starttag_span_outside_code_no_error(self):
        self.parser.handle_starttag("span", [])
        self.assertFalse(self.parser.parser_error)
        self.assertEqual(self.parser.output[0], "<span>")

    def test_starttag_pre_in_code_sets_error(self):
        self.parser.is_code = True
        # prior output whose last element is not a <code ...> tag, so the
        # <pre>-insert branch is skipped but the error flag is still set
        self.parser.output.append("some text")
        self.parser.handle_starttag("pre", [])
        self.assertTrue(self.parser.parser_error)

    def test_starttag_pre_outside_code_no_error(self):
        self.parser.handle_starttag("pre", [])
        self.assertFalse(self.parser.parser_error)
        self.assertEqual(self.parser.output[0], "<pre>")

    def test_starttag_span_in_code_verify_prints_warning(self):
        self.parser.verify = True
        self.parser.is_code = True
        with redirect_stdout(io.StringIO()) as buf:
            self.parser.handle_starttag("span", [])
        self.assertTrue(self.parser.parser_error)
        self.assertIn("[WARNING]", buf.getvalue())
        self.assertIn("<span>", buf.getvalue())

    def test_starttag_pre_in_code_verify_prints_warning(self):
        self.parser.verify = True
        self.parser.is_code = True
        self.parser.output.append("some text")
        with redirect_stdout(io.StringIO()) as buf:
            self.parser.handle_starttag("pre", [])
        self.assertTrue(self.parser.parser_error)
        self.assertIn("[WARNING]", buf.getvalue())
        self.assertIn("misalligned", buf.getvalue())

    def test_starttag_pre_in_code_inserts_pre_before_code(self):
        self.parser.is_code = True
        # simulate a prior <code ...> being the last output entry
        self.parser.output.append('<code class="language-cpp">')
        self.parser.handle_starttag("pre", [])
        # <pre> gets inserted before the last element
        self.assertEqual(self.parser.output[-2], "<pre>")
        self.assertEqual(self.parser.output[-1], '<code class="language-cpp">')

    def test_starttag_disallowed_tag_in_code(self):
        self.parser.is_code = True
        self.parser.handle_starttag("div", [])
        self.assertTrue(self.parser.parser_error)
        # emitted escaped
        self.assertEqual(self.parser.output[0], "&lt;div&gt;")

    def test_starttag_disallowed_tag_uses_raw_starttag_text(self):
        # feed the full document so get_starttag_text() returns the raw text
        self.parser.feed('<code><DIV class="x">y</DIV></code>')
        # the escaped raw tag (original case + attrs) should be present
        joined = "".join(self.parser.output)
        self.assertIn('&lt;DIV class="x"&gt;', joined)

    # ---------------------------------------------------------------------
    # handle_data
    # ---------------------------------------------------------------------

    def test_handle_data_outside_code(self):
        self.parser.handle_data("hello")
        self.assertEqual(self.parser.output, ["hello"])
        self.assertEqual(self.parser.code_blocks, [])

    def test_handle_data_in_code_without_extract(self):
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_data("int x;")
        # data still goes to output, but not accumulated into code_blocks
        self.assertEqual(self.parser.output, ["int x;"])
        self.assertEqual(self.parser.code_blocks[-1][1], "")

    def test_handle_data_in_code_with_extract(self):
        self.parser.extract = True
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_data("int x;")
        self.assertEqual(self.parser.code_blocks[-1][1], "int x;")
        self.assertEqual(self.parser.output, ["int x;"])

    def test_handle_data_appends_across_calls(self):
        self.parser.extract = True
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_data("int ")
        self.parser.handle_data("x;")
        self.assertEqual(self.parser.code_blocks[-1][1], "int x;")

    # ---------------------------------------------------------------------
    # handle_entityref
    # ---------------------------------------------------------------------

    def test_handle_entityref_outside_code(self):
        self.parser.handle_entityref("lt")
        self.assertEqual(self.parser.output, ["&lt;"])

    def test_handle_entityref_in_code_with_extract_unescapes(self):
        self.parser.extract = True
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_entityref("lt")
        # raw entity preserved in output
        self.assertEqual(self.parser.output, ["&lt;"])
        # but the code block gets the unescaped char
        self.assertEqual(self.parser.code_blocks[-1][1], "<")

    def test_handle_entityref_in_code_without_extract(self):
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_entityref("amp")
        self.assertEqual(self.parser.output, ["&amp;"])
        self.assertEqual(self.parser.code_blocks[-1][1], "")

    # ---------------------------------------------------------------------
    # handle_charref
    # ---------------------------------------------------------------------

    def test_handle_charref_outside_code(self):
        self.parser.handle_charref("60")
        self.assertEqual(self.parser.output, ["&#60;"])

    def test_handle_charref_in_code_with_extract_unescapes(self):
        self.parser.extract = True
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_charref("60")
        self.assertEqual(self.parser.output, ["&#60;"])
        self.assertEqual(self.parser.code_blocks[-1][1], "<")

    def test_handle_charref_in_code_without_extract(self):
        self.parser.is_code = True
        self.parser.code_blocks.append(((1, 0), ""))
        self.parser.handle_charref("62")
        self.assertEqual(self.parser.output, ["&#62;"])
        self.assertEqual(self.parser.code_blocks[-1][1], "")

    # ---------------------------------------------------------------------
    # handle_startendtag
    # ---------------------------------------------------------------------

    def test_code_startendtag_extract(self):
        self.parser.extract = True
        self.parser.handle_startendtag("link", [("rel", "stylesheet")])
        self.assertEqual(self.parser.output[0], '<link rel="stylesheet">')

    def test_startendtag_without_extract_emits_nothing(self):
        self.parser.handle_startendtag("link", [("rel", "stylesheet")])
        self.assertEqual(self.parser.output, [])

    def test_startendtag_extract_no_attrs(self):
        self.parser.extract = True
        self.parser.handle_startendtag("br", [])
        self.assertEqual(self.parser.output[0], "<br>")

    # ---------------------------------------------------------------------
    # handle_endtag
    # ---------------------------------------------------------------------

    def test_endtag_code_resets_flags(self):
        self.parser.is_code = True
        self.parser.is_mark = True
        self.parser.handle_endtag("code")
        self.assertFalse(self.parser.is_code)
        self.assertFalse(self.parser.is_mark)
        self.assertEqual(self.parser.output[-1], "</code>")

    def test_endtag_code_case_insensitive(self):
        self.parser.is_code = True
        self.parser.handle_endtag("CODE")
        self.assertFalse(self.parser.is_code)
        # output preserves original case
        self.assertEqual(self.parser.output[-1], "</CODE>")

    def test_endtag_non_code(self):
        self.parser.is_code = True
        self.parser.handle_endtag("span")
        # non-code endtag does not reset the code flag
        self.assertTrue(self.parser.is_code)
        self.assertEqual(self.parser.output[-1], "</span>")

    # ---------------------------------------------------------------------
    # Integration: feed() end-to-end
    # ---------------------------------------------------------------------

    def test_feed_simple_code_block_extract(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("<code>int a = 1;</code>")
        self.assertEqual(len(parser.code_blocks), 1)
        self.assertEqual(parser.code_blocks[0][1], "int a = 1;")
        self.assertFalse(parser.parser_error)

    def test_feed_code_with_entities_extract(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("<code>a &lt; b &amp;&amp; c &gt; d</code>")
        self.assertEqual(parser.code_blocks[0][1], "a < b && c > d")
        # output keeps the raw entities
        self.assertIn("&lt;", "".join(parser.output))

    def test_feed_code_with_charref_extract(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("<code>a&#60;b</code>")
        self.assertEqual(parser.code_blocks[0][1], "a<b")

    def test_feed_mark_in_code_is_allowed(self):
        parser = LessonChecker.SYCLAParser("L", extract=False, verify=False)
        parser.feed("<code>a<mark>b</mark>c</code>")
        self.assertFalse(parser.parser_error)

    def test_feed_span_in_code_flags_error(self):
        parser = LessonChecker.SYCLAParser("L", extract=False, verify=False)
        parser.feed("<code><span>x</span></code>")
        self.assertTrue(parser.parser_error)

    def test_feed_disallowed_tag_in_code_flags_error(self):
        parser = LessonChecker.SYCLAParser("L", extract=False, verify=False)
        parser.feed("<code><div>x</div></code>")
        self.assertTrue(parser.parser_error)

    def test_feed_multiple_code_blocks(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("<code>one</code><p>text</p><code>two</code>")
        self.assertEqual(len(parser.code_blocks), 2)
        self.assertEqual(parser.code_blocks[0][1], "one")
        self.assertEqual(parser.code_blocks[1][1], "two")

    def test_feed_records_position_of_code_block(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("line1\n<code>x</code>")
        # position is (line, offset); code opens on line 2
        pos = parser.code_blocks[0][0]
        self.assertEqual(pos[0], 2)

    def test_feed_data_outside_code_not_extracted(self):
        parser = LessonChecker.SYCLAParser("L", extract=True, verify=False)
        parser.feed("<p>hello</p>")
        self.assertEqual(parser.code_blocks, [])

    def test_feed_roundtrip_preserves_output_for_clean_html(self):
        # a code block with only a mark should round-trip (aside from the
        # injected language-cpp class)
        parser = LessonChecker.SYCLAParser("L", extract=False, verify=False)
        parser.feed('<code class="language-cpp">a<mark>b</mark></code>')
        self.assertEqual(
            "".join(parser.output),
            '<code class="language-cpp">a<mark>b</mark></code>',
        )


class TestCLIIntegration(unittest.TestCase):
    """End-to-end tests that run LessonChecker.py as a script."""

    SCRIPT = str(Path(LessonChecker.__file__).resolve())
    SCRIPT_DIR = str(Path(LessonChecker.__file__).resolve().parent)

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _make_lesson(self, name, html):
        """Create <root>/<name>/index.html and return the lesson dir path."""
        lesson_dir = self.root / name
        lesson_dir.mkdir(parents=True, exist_ok=True)
        (lesson_dir / "index.html").write_text(html, encoding="utf-8")
        return lesson_dir

    def _run(self, *cli_args):
        # Propagate the coverage settings so the spawned interpreter records
        # its own data (via sitecustomize.py + coverage.process_startup()).
        # This is a no-op when coverage is not driving the tests.
        env = os.environ.copy()
        if env.get("COVERAGE_PROCESS_START"):
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = (
                self.SCRIPT_DIR + os.pathsep + existing if existing else self.SCRIPT_DIR
            )
        return subprocess.run(
            [sys.executable, self.SCRIPT, *cli_args],
            capture_output=True,
            text=True,
            env=env,
        )

    # ---------------------------------------------------------------------

    def test_no_arguments_does_nothing(self):
        result = self._run()
        self.assertEqual(result.returncode, 0)
        self.assertIn("nothing to do", result.stdout)

    def test_extract_without_output_errors(self):
        lesson = self._make_lesson("L", "<code>x</code>")
        result = self._run("--extract", "--files", str(lesson))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output must be specified", result.stderr)

    def test_missing_lesson_raises(self):
        missing = self.root / "does_not_exist"
        result = self._run("--verify", "--files", str(missing))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_verify_clean_lesson_reports_no_issues(self):
        lesson = self._make_lesson("Clean", "<code>int a = 1;</code>")
        result = self._run("--verify", "--files", str(lesson))
        self.assertEqual(result.returncode, 0)
        self.assertIn("No issues found.", result.stdout)

    def test_verify_flags_span_in_code(self):
        lesson = self._make_lesson("Bad", "<code><span>x</span></code>")
        result = self._run("--verify", "--files", str(lesson))
        self.assertEqual(result.returncode, 0)
        self.assertIn("[WARNING]", result.stdout)
        # a lesson with issues should not print the all-clear message
        self.assertNotIn("No issues found.", result.stdout)

    def test_extract_writes_cpp_files(self):
        lesson = self._make_lesson("Ex", "<code>int a &lt; b;</code>")
        out_dir = self.root / "out"
        result = self._run(
            "--extract",
            "--files",
            str(lesson),
            "--output",
            str(out_dir),
        )
        self.assertEqual(result.returncode, 0)
        cpp_files = list(out_dir.glob("*.cpp"))
        self.assertEqual(len(cpp_files), 1)
        # entities should be unescaped in the extracted source
        self.assertEqual(cpp_files[0].read_text(), "int a < b;")
        self.assertTrue(cpp_files[0].name.startswith("Ex-"))

    def test_extract_multiple_code_blocks(self):
        lesson = self._make_lesson("Multi", "<code>one</code><p>x</p><code>two</code>")
        out_dir = self.root / "out"
        result = self._run(
            "--extract", "--files", str(lesson), "--output", str(out_dir)
        )
        self.assertEqual(result.returncode, 0)
        contents = sorted(p.read_text() for p in out_dir.glob("*.cpp"))
        self.assertEqual(contents, ["one", "two"])

    def test_extract_multiple_lessons(self):
        a = self._make_lesson("A", "<code>aaa</code>")
        b = self._make_lesson("B", "<code>bbb</code>")
        out_dir = self.root / "out"
        result = self._run(
            "--extract",
            "--files",
            str(a),
            str(b),
            "--output",
            str(out_dir),
        )
        self.assertEqual(result.returncode, 0)
        contents = sorted(p.read_text() for p in out_dir.glob("*.cpp"))
        self.assertEqual(contents, ["aaa", "bbb"])

    def test_autofix_rewrites_index_html(self):
        html = "<code>int a = 1;</code>"
        lesson = self._make_lesson("Fix", html)
        result = self._run(
            "--autofix",
            "--files",
            str(lesson),
            "--output",
            str(self.root / "out"),
        )
        self.assertEqual(result.returncode, 0)
        rewritten = (lesson / "index.html").read_text()
        # autofix injects the language-cpp class onto <code> tags
        self.assertIn('<code class="language-cpp">', rewritten)

    def test_mutually_exclusive_modes_rejected(self):
        lesson = self._make_lesson("L", "<code>x</code>")
        result = self._run("--verify", "--extract", "--files", str(lesson))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not allowed with", result.stderr)
