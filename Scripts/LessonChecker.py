# SYCL academy lesson checker and code extractor
# Michael Lance
# June 2026

# ------------------------------------------------------------------------------------------

from html.parser import HTMLParser
from pathlib import Path
import sys

# ------------------------------------------------------------------------------------------
# Config

base_path = Path("../Lesson_Materials/")
out_base = Path("out")

# ------------------------------------------------------------------------------------------


class AParser(HTMLParser):
    def __init__(self, lesson_name: str):
        super().__init__()

        self.code_blocks = []
        self.output = []
        self.is_code = False
        self.is_mark = False
        self.lesson_name = lesson_name

    def handle_starttag(self, tag, attrs):
        attrd = dict(attrs)

        match tag.lower():
            case "code":
                self.is_code = True
                attrd["class"] = "language-cpp"
            case "mark":
                self.is_mark = True
            case "span":
                if self.is_code:
                    print(
                        f"\033[93m[WARNING] <span> used in <code> for highlight instead of <mark> in lesson {self.lesson_name} line num: {self.getpos()} \033[0m"
                    )
            case "pre":
                if self.is_code:
                    print(
                        f"\033[93m[FIXING] misalligned <code> and <pre> tags in lesson {self.lesson_name} line num: {self.getpos()} \033[0m"
                    )
                    print(self.output[-1])
                    if "code" in self.output[-1]:
                        self.output.append(self.output[-1])
                        self.output[-2] = "<pre>"
                        return
            case _:
                if self.is_code:
                    print(
                        f"\033[93m[WARNING] <mark> annotations are the only tags allowed in <code> blocks! Violation in lesson {self.lesson_name} line num: {self.getpos()} tag: {tag} \033[0m"
                    )
                    self.output.append(f"&lt;{tag}&gt;")
                    return

        attr_str = "".join([f' {k}="{v}"' for k, v in attrd.items()])
        self.output.append(f"<{tag}{attr_str}>")

    def handle_data(self, data):
        if self.is_code and not self.is_mark:
            self.code_blocks.append(data)
        elif self.is_code and self.is_mark:
            self.code_blocks[-1] += data

        self.output.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "code":
            self.is_code = False
            self.is_mark = False

        self.output.append(f"</{tag}>")


# ------------------------------------------------------------------------------------------

for lesson in sys.argv[1:]:
    print(f"processing lesson: {lesson}...")

    in_path = base_path / lesson / "index.html"
    write_back_path = in_path

    if not in_path.exists():
        continue

    with open(in_path, "r", encoding="utf-8") as file:
        parser = AParser(lesson)

        try:
            parser.feed(file.read())
        except Exception as e:
            print(e)

        # print("".join(parser.output))
        out_path = out_base / lesson

        out_path.mkdir(parents=True, exist_ok=True)

        for idx, code in enumerate(parser.code_blocks):
            name = f"{out_path}/{idx}.cpp"

            with open(name, "w") as out:
                out.write(code)

        with open(write_back_path, "w") as out:
            out.write("".join(parser.output))
