# SYCL academy lesson checker and code extractor
# Michael Lance
# June 2026

# ------------------------------------------------------------------------------------------

import html
from html.parser import HTMLParser
from pathlib import Path
import argparse
import sys
from typing import cast

# ------------------------------------------------------------------------------------------
# Config

aparser = argparse.ArgumentParser()

opgroup = aparser.add_mutually_exclusive_group()

opgroup.add_argument("-v", "--verify", action="store_true")
opgroup.add_argument("-e", "--extract", action="store_true")
opgroup.add_argument("-a", "--autofix", action="store_true")

aparser.add_argument("files", nargs=argparse.REMAINDER)
aparser.add_argument("-o", "--output")

# ------------------------------------------------------------------------------------------


class SYCLAParser(HTMLParser):
    VOID_ELEMENTS = {
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

    def __init__(self, lesson_name: str, extract: bool, verify: bool, fix: bool):
        super().__init__(convert_charrefs=False)

        self.code_blocks: list[tuple[int, str]] = []
        self.output: list[str] = []
        self.is_code = False
        self.is_mark = False
        self.parser_error = False
        self.lesson_name = lesson_name

        self.extract = extract
        self.verify = verify
        self.fix = fix

        self.msg_action = "FIXING" if self.fix else "ERROR"

    def handle_starttag(self, tag, attrs):
        attrd = dict(attrs)

        match tag:
            case "code":
                self.is_code = True
                attrd["class"] = "language-cpp"
                self.code_blocks.append((self.getpos()[0], ""))
            case "mark":
                self.is_mark = True
            case "pre":
                if self.is_code:
                    self.parser_error = True
                    print(
                        f"\033[93m[{self.msg_action}] misalligned <code> and <pre> tags in lesson {self.lesson_name} line num: {self.getpos()[0]} \033[0m"
                    )

                    if "code" in self.output[-1]:

                        self.output.insert(-1, "<pre>")
                        return
            case _:
                if self.is_code:
                    self.parser_error = True
                    print(
                        f"\033[93m[{self.msg_action}] <mark> annotations are the only tags allowed in <code> blocks! Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag} \033[0m"
                    )
                    self.convert_charrefs = False

                    # Fetch the original case of the impropperly escaped code
                    raw_tag = self.get_starttag_text()

                    self.output.append(
                        f"&lt;{cast(str, raw_tag).lstrip("<").rstrip(">")}&gt;"
                    )
                    return

        tags = [tag] + [
            f"{k}" if v in [None, True] else f'{k}="{v.strip()}"'  # pyright: ignore
            for k, v in attrd.items()
        ]

        self.output.append(f"<{' '.join(tags)}>")

    def handle_data(self, data):
        if self.is_code and self.extract:
            pos, e_data = self.code_blocks[-1]
            self.code_blocks[-1] = (pos, e_data + data)

        self.output.append(data)

    def handle_entityref(self, name):

        match name:
            case "lt" | "gt" | "amp":
                raw_entity = f"&{name};"

            case _:
                self.parser_error = True
                print(
                    f"\033[93m[{self.msg_action}] Impropperly escaped entity ref! Violation in lesson {self.lesson_name} line num: {self.getpos()} ref: {name} \033[0m")

                raw_entity = f"&amp;{name}"

        self.output.append(raw_entity)

        if self.is_code and self.extract:
            converted_char = html.unescape(raw_entity)
            pos, e_data = self.code_blocks[-1]
            self.code_blocks[-1] = (pos, e_data + converted_char)

    def handle_startendtag(self, tag, attrs):
        attrd = dict(attrs)
        tags = [tag] + [
            f"{k}" if v in [None, True] else f'{k}="{v.strip()}"'  # pyright: ignore
            for k, v in attrd.items()
        ]

        self.output.append(f"<{' '.join(tags)} />")

    def handle_endtag(self, tag):
        if tag in self.VOID_ELEMENTS:
            self.parser_error = True
            print(
                f"\033[93m[{self.msg_action}] Self closing tag does not require an endtag Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag} \033[0m"
            )
            return

        if tag == "code":
            self.is_code = False
            self.is_mark = False

        self.output.append(f"</{tag}>")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")

    def get_output(self):
        return "".join(self.output)

    def get_codeblocks(self):
        return self.code_blocks

# ------------------------------------------------------------------------------------------


def verify_html(lesson, file_str, args) -> tuple[str, list, bool]:
    parser = SYCLAParser(lesson, args.extract, args.verify, args.autofix)
    parser.feed(file_str)

    return parser.get_output(), parser.get_codeblocks(), parser.parser_error


# ------------------------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    args = aparser.parse_args()

    if not any([args.extract, args.autofix, args.verify]):
        print("No arguments provided. There is nothing to do.")
        sys.exit()

    if args.extract and not args.output:
        raise Exception("Error: An output must be specified with -o or --output")


    out_base = Path(args.output or "")
    cmake_executables = ""
    
    verify_failed = False

    for lesson in args.files:
        print(f"processing lesson: {lesson}...")
        l_path = Path(lesson)
        print(f"l_path: {l_path.parent.name}")

        if not l_path.exists():
            msg = f'Lesson "{lesson}" does not exist!'
            raise Exception(msg)

        with open(l_path, "r", encoding="utf-8") as file:
            # use verify_html here 
            parser = SYCLAParser(lesson, args.extract, args.verify, args.autofix)
            parser.feed(file.read())

            if args.verify:
                if parser.parser_error:
                    verify_failed = True
                else:
                    print("No issues found.")

            if args.extract:
                out_base.mkdir(parents=True, exist_ok=True)

                for pos, code in parser.code_blocks:
                    name = f"{l_path.parent.name}-l{pos}.cpp" 

                    cmake_executables += f"add_sycl_executable(Lesson_Snippets {name})\n"

                    wpath = f"{out_base}/{l_path.parent.name}-l{pos}.cpp"

                    print(f"Exporting script: {wpath}")
                    with open(wpath, "w") as out:
                        out.write(code)

            with open(f"{out_base}/CMakeLists.txt", "w") as cmake:
                cmake.write(cmake_executables)

            if args.autofix:
                write_back_path = l_path

                with open(write_back_path, "w") as out:
                    out.write(parser.get_output())

    if verify_failed:
        sys.exit(1)
