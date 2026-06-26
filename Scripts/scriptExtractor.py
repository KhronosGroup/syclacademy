# SYCL academy code example extractor
# Michael Lance
# June 2026

from html.parser import HTMLParser
from pathlib import Path

# ------------------------------------------------------------------------------------------
# Config

base_path = Path("../Lesson_Materials/")
out_base = Path("out")

# ------------------------------------------------------------------------------------------

class CodeExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.code_blocks = []
        self.is_code = False
        self.is_mark = False

    def handle_starttag(self, tag, attrs):
        match tag.lower(): 
            case 'code':
                self.is_code = True 
            case 'mark':
                self.is_mark = True
            case 'pre':
                # TODO: check how to get file name into here
                if self.is_code:
                    print("invalid tag arrangemnt in file")
            case _:
                if self.is_code:
                    msg = f"Mark is the only tag allowed in a codeblock! line num: {self.getpos()} tag: {tag}"
                    raise Exception(msg)

    def handle_data(self, data):
        if self.is_code and not self.is_mark:
            self.code_blocks.append(data)
        elif self.is_code and self.is_mark:
            self.code_blocks[-1] += data

    def handle_endtag(self, tag):
        if tag.lower() == 'code':
            self.is_code = False
            self.is_mark = False

# ------------------------------------------------------------------------------------------


print("Checking all code examples compile with icpx")
for lesson in base_path.glob("*/"):
    print(f"processing lesson: {lesson}...")

    in_path = base_path / f"{lesson.name}" / "index.html"

    if not in_path.exists():
        continue

    with open(in_path, "r", encoding="utf-8") as file:
        parser = CodeExtractor()

        parser.feed(file.read())
        out_path = out_base / lesson.name

        out_path.mkdir(parents=True, exist_ok=True)

        for idx, code in enumerate(parser.code_blocks):
            name = f"{out_path}/{idx}.cpp"

            with open(name, "w") as out:
                out.write(code)
