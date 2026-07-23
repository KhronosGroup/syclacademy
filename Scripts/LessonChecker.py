# SYCL academy lesson checker and code extractor
# Michael Lance
# July 2026

# ------------------------------------------------------------------------------------------

import html
from html.parser import HTMLParser
from dataclasses import dataclass, field
from enum import IntFlag, auto
from pathlib import Path
import argparse
import sys
import re

# ------------------------------------------------------------------------------------------
# Config

aparser = argparse.ArgumentParser()

opgroup = aparser.add_mutually_exclusive_group()

# Autofix and extract operations are always performed, these flags control whether its written to disk
opgroup.add_argument("-v", "--verify", action="store_true")
opgroup.add_argument("-e", "--extract", action="store_true")
opgroup.add_argument("-a", "--autofix", action="store_true")

aparser.add_argument("files", nargs=argparse.REMAINDER)
aparser.add_argument("-o", "--output")
aparser.add_argument("-s", "--silent", action="store_true")

# ANSI color codes for output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# ------------------------------------------------------------------------------------------


class Mode(IntFlag):
    NONE = 0
    EXTRACT = auto()
    VERIFY = auto()
    AUTOFIX = auto()
    SILENT = auto()


class State(IntFlag):
    NONE = 0
    CODE = auto()
    MARK = auto()
    ERROR = auto()


# ------------------------------------------------------------------------------------------


@dataclass
class SYCLAParser(HTMLParser):
    lesson_name: str
    mode: Mode
    code_blocks: list[tuple[int, str]] = field(default_factory=list)
    output: list[str] = field(default_factory=list)

    state: State = State.NONE

    SELF_CLOSING_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    COLORS = {Mode.VERIFY: YELLOW, Mode.AUTOFIX: GREEN}

    def __post_init__(self):
        # call the constructor for the parent class
        # Tell the HTMLParser base class to not convert character references
        super().__init__(convert_charrefs=False)

    @property
    def msg_action(self):
        return "FIXING" if self.mode & Mode.AUTOFIX else "ERROR"

    @property
    def output_joined(self):
        return "".join(self.output)

    @property
    def parser_error(self):
        return State.ERROR in self.state

    @property
    def last_code_idx(self):
        if State.CODE in self.state:
            # reverse search output for last code tag
            return next(
                (
                    i
                    for i in range(len(self.output) - 1, -1, -1)
                    # < is important, because the word "code" can apepar in a comment, just like it does in this one
                    if "<code" in self.output[i]
                ),
                None,
            )

    def _encode_attrs(self, tag, attrs):
        tag_attrs = [tag] + [
            f"{k}" if v in [None, True] else f'{k}="{v.strip()}"'  # pyright: ignore
            for k, v in attrs
        ]

        if tag in self.SELF_CLOSING_TAGS:
            return f"<{' '.join(tag_attrs)}/>"
        else:
            return f"<{' '.join(tag_attrs)}>"

    def _warn(self, message):
        if self.mode & Mode.SILENT:
            return

        if bool(self.mode & (Mode.AUTOFIX | Mode.VERIFY)):
            print(f"{self.COLORS[self.mode]}[{self.msg_action}] {message} {RESET}")

    def handle_starttag(self, tag, attrs):
        match tag:
            case "code":
                self.state |= State.CODE

                if ("class", "language-cpp") not in attrs:
                    self.state |= State.ERROR
                    self._warn(
                        f"highlight langauge class missing in lesson {self.lesson_name} line num: {self.getpos()[0]}"
                    )
                    attrs.append(("class", "language-cpp"))

                if ("class", "code-100pc") in attrs:
                    self.state |= State.ERROR
                    self._warn(
                        f"Old stling in lesson {self.lesson_name} line num: {self.getpos()[0]}"
                    )
                    attrs.remove(("class", "code-100pc"))

                self.code_blocks.append((self.getpos()[0], ""))

            case "mark":
                self.state |= State.MARK

                # cache the last code
                last_code_idx = self.last_code_idx

                if (
                    State.CODE in self.state
                    and last_code_idx is not None
                    and "data-noescape" not in self.output[last_code_idx]
                ):
                    self.state |= State.ERROR
                    self._warn(
                        f"<mark> in <code> without data-noescape prop in lesson {self.lesson_name} line num: {self.getpos()[0]}"
                    )

                    # Add data-noescape prop to code
                    code_tag = self.output[last_code_idx]
                    self.output[last_code_idx] = (
                        code_tag[:-1] + " data-noescape" + code_tag[-1]
                    )

            case "pre" if State.CODE in self.state:

                self.state |= State.ERROR
                self._warn(
                    f"misalligned <code> and <pre> tags in lesson {self.lesson_name} line num: {self.getpos()[0]}"
                )

                if "code" in self.output[-1]:
                    self.output.insert(-1, "<pre>")
                    return

            case _:
                # Any other unescaped
                if State.CODE in self.state:
                    self.state |= State.ERROR
                    self._warn(
                        f"<mark> annotations are the only tags allowed in <code> blocks! Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag}"
                    )

                    # Fetch the original case of the impropperly escaped code
                    raw_tag = self.get_starttag_text()

                    self.output.append(
                        f"&lt;{raw_tag.lstrip("<").rstrip(">")}&gt;"  # pyright: ignore
                    )
                    return

        self.output.append(self._encode_attrs(tag, attrs))

    def handle_data(self, data):
        if State.CODE in self.state and bool(self.mode & Mode.EXTRACT):
            pos, e_data = self.code_blocks[-1]
            self.code_blocks[-1] = (pos, e_data + data)

        if any((viol_char := char) in {"&", "<", ">"} for char in data):
            self.state |= State.ERROR
            self._warn(
                f"Unescaped character {viol_char} in lesson {self.lesson_name} line num: {self.getpos()[0]}"
            )

        data = data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        self.output.append(data)

    def handle_entityref(self, name):
        match name:
            case "lt" | "gt" | "amp":
                raw_entity = f"&{name};"

            case str() if m := re.search(r"(lt|gt|amp)(.+)", name):
                raw_entity = f"&{m.group(1)};{m.group(2)}"

                self.state |= State.ERROR
                self._warn(
                    f"Partial escape sequence found in lesson {self.lesson_name} line num: {self.getpos()[0]}"
                )
            case _:
                self.state |= State.ERROR
                self._warn(
                    f"Impropperly escaped entity ref! Violation in lesson {self.lesson_name} line num: {self.getpos()} ref: {name}"
                )

                raw_entity = f"&amp;{name}"

        self.output.append(raw_entity)

        if State.CODE in self.state and bool(self.mode & Mode.EXTRACT):
            converted_char = html.unescape(raw_entity)
            pos, e_data = self.code_blocks[-1]
            self.code_blocks[-1] = (pos, e_data + converted_char)

    def handle_startendtag(self, tag, attrs):
        self.output.append(self._encode_attrs(tag, attrs))

    def handle_endtag(self, tag):
        if tag in self.SELF_CLOSING_TAGS:
            self.state |= State.ERROR
            self._warn(
                f"Self closing tag does not require an endtag Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag}"
            )
            return

        match tag:
            case "code":
                self.state &= ~State.CODE
            case "mark":
                self.state &= ~State.MARK

        self.output.append(f"</{tag}>")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")


# -----------------------------------------------------------------------------------------


def verify_html(lesson, file_str, args) -> tuple[str, list, bool]:
    mode = Mode.NONE

    for key, value in vars(args).items():
        if value and key not in {"files", "output"}:
            mode |= getattr(Mode, key.upper())

    parser = SYCLAParser(lesson, mode)
    parser.feed(file_str)

    return parser.output_joined, parser.code_blocks, parser.parser_error


# ------------------------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    args = aparser.parse_args()

    if not any([args.extract, args.autofix, args.verify]):
        print("No arguments provided. There is nothing to do.")
        sys.exit(1)

    if args.extract and not args.output:
        raise Exception("Error: An output must be specified with -o or --output")

    out_base = Path(args.output or "")
    cmake_executables = ""

    verify_failed = False

    for lesson in args.files:
        print(f"processing lesson: {lesson}...")
        l_path = Path(lesson)

        if not l_path.exists():
            msg = f'Lesson "{lesson}" does not exist!'
            raise Exception(msg)

        with open(l_path, "r", encoding="utf-8") as file:

            output, code_blocks, error = verify_html(lesson, file.read(), args)

            if args.verify:
                if error:
                    verify_failed = True
                else:
                    print("No issues found.")

            if args.extract:
                out_base.mkdir(parents=True, exist_ok=True)

                for pos, code in code_blocks:
                    name = f"{l_path.parent.name}-l{pos}"

                    cmake_executables += (
                        f"add_sycl_executable(Lesson_Snippets {name})\n"
                    )

                    wpath = f"{out_base}/{name}.cpp"

                    print(f"Exporting script: {wpath}")
                    with open(wpath, "w") as out:
                        out.write(code)

                with open(f"{out_base}/CMakeLists.txt", "w") as cmake:
                    cmake.write(cmake_executables)

            # only write back to file if there is sonething to fix
            if args.autofix and error:
                print("Saving fixes back to lesson")
                write_back_path = l_path

                with open(write_back_path, "w") as out:
                    out.write(output)

    if verify_failed:
        sys.exit(1)
