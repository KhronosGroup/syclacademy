# SYCL academy lesson checker and code extractor
# Michael Lance
# June 2026

# ------------------------------------------------------------------------------------------

import html
from html.parser import HTMLParser
from pathlib import Path
import argparse
import sys

# ------------------------------------------------------------------------------------------
# Config

aparser = argparse.ArgumentParser()

opgroup = aparser.add_mutually_exclusive_group()

opgroup.add_argument("-v", "--verify", action="store_true")
opgroup.add_argument("-e", "--extract", action="store_true")
opgroup.add_argument("-a", "--autofix", action="store_true")

aparser.add_argument("-f", "--files", nargs="*")
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

    def __init__(self, lesson_name: str, extract: bool, verify: bool):
        super().__init__(convert_charrefs=False)

        self.code_blocks: list[tuple[tuple[int, int], str]] = []
        self.output: list[str] = []
        self.is_code = False
        self.is_mark = False
        self.parser_error = False
        self.lesson_name = lesson_name

        self.extract = extract
        self.verify = verify

    def handle_starttag(self, tag, attrs):
        attrd = dict(attrs)

        match tag:
            case "code":
                self.is_code = True
                attrd["class"] = "language-cpp"
                self.code_blocks.append((self.getpos(), ""))
            case "mark":
                self.is_mark = True
            case "span":
                if self.is_code:
                    self.parser_error = True
                    if self.verify:
                        print(
                            f"\033[93m[WARNING] <span> used in <code> for highlight instead of <mark> in lesson {self.lesson_name} line num: {self.getpos()} \033[0m"
                        )
            case "pre":
                if self.is_code:
                    self.parser_error = True
                    if self.verify:
                        print(
                            f"\033[93m[WARNING] misalligned <code> and <pre> tags in lesson {self.lesson_name} line num: {self.getpos()} \033[0m"
                        )

                    if "code" in self.output[-1]:

                        self.output.insert(-1, "<pre>")
                        return
            case _:
                if self.is_code:
                    self.parser_error = True
                    print(
                        f"\033[93m[WARNING] <mark> annotations are the only tags allowed in <code> blocks! Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag} \033[0m"
                    )
                    self.convert_charrefs = False

                    # Fetch the original case of the impropperly escaped code
                    raw_tag = self.get_starttag_text()

                    if not raw_tag:
                        raw_tag = tag

                    self.output.append(f"&lt;{raw_tag.lstrip("<").rstrip(">")}&gt;")
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
        raw_entity = f"&{name};"

        self.output.append(raw_entity)

        if self.is_code and self.extract:
            converted_char = html.unescape(raw_entity)
            pos, e_data = self.code_blocks[-1]
            self.code_blocks[-1] = (pos, e_data + converted_char)

    def handle_charref(self, name):
        raw_entity = f"&#{name};"

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
        if tag.lower() in self.VOID_ELEMENTS:
            return

        if tag.lower() == "code":
            self.is_code = False
            self.is_mark = False

        self.output.append(f"</{tag}>")

    def handle_comment(self, data):
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")


# ------------------------------------------------------------------------------------------


if __name__ == "__main__":
    args = aparser.parse_args()

    if not any([args.extract, args.autofix, args.verify]):
        print("No arguments provided. There is nothing to do.")
        sys.exit()

    if args.extract and not args.output:
        raise Exception("Error: An output must be specified with -o or --output")

    out_base = Path(args.output or "")

    for lesson in args.files:
        print(f"processing lesson: {lesson}...")
        l_path = Path(lesson)

        in_path = l_path / "index.html"

        if not in_path.exists():
            msg = f'Lesson "{lesson}" does not exist!'
            raise Exception(msg)

        with open(in_path, "r", encoding="utf-8") as file:
            parser = SYCLAParser(lesson, args.extract, args.verify)
            parser.feed(file.read())

            if not parser.parser_error:
                print("No issues found.")

            if args.extract:
                out_base.mkdir(parents=True, exist_ok=True)

                for pos, code in parser.code_blocks:
                    name = f"{out_base}/{l_path.name}-{pos[0]}-{pos[1]}.cpp"

                    print(f"Exporting script: {name}")
                    with open(name, "w") as out:
                        out.write(code)

            if args.autofix:
                write_back_path = in_path

                with open(write_back_path, "w") as out:
                    out.write("".join(parser.output))
