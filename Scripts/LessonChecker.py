# SYCL academy lesson checker and code extractor
# Michael Lance
# June 2026

# ------------------------------------------------------------------------------------------

from pathlib import Path
from parsers import CodeExtractor
import sys

# ------------------------------------------------------------------------------------------
# Config

base_path = Path("../Lesson_Materials/")
out_base = Path("out")

# ------------------------------------------------------------------------------------------

for lesson in sys.argv[1:]:
    print(f"processing lesson: {lesson}...")

    in_path = base_path / lesson / "index.html"

    if not in_path.exists():
        continue

    with open(in_path, "r", encoding="utf-8") as file:
        parser = CodeExtractor(lesson)

        try:
            parser.feed(file.read())
        except Exception as e:
            print(e)

        print("".join(parser.output))
        out_path = out_base / lesson

        out_path.mkdir(parents=True, exist_ok=True)

        for idx, code in enumerate(parser.code_blocks):
            name = f"{out_path}/{idx}.cpp"

            with open(name, "w") as out:
                out.write(code)
