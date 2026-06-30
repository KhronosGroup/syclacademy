from html.parser import HTMLParser

# ------------------------------------------------------------------------------------------


class Reformatter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)

        self.output = []
        self.nested_level = 0
        self.parents = []
        self.invalid = False
        self.excluded_tags = {"link", "meta"}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if len(self.output) == 0 or tag in self.excluded_tags:
            self.output.append(f"<{tag}>")
            return

        if "code" in self.parents:
            match tag:
                case "pre":
                    self.invalid = True
                    self.output.append(self.output[-1])
                    self.output[-2] = "<pre>"
                    return
                case "mark":
                    # mark tags are valid inside code blocks
                    pass
                case "span":
                    pass
                case _:
                    print(f"{tag} found in <code>")
                    self.invalid = True
                    self.output.append(f"&lt;{tag}&gt;")

        if not self.output[-1].startswith("</"):
            self.nested_level += 1
            self.parents.append(tag)

        if tag == "code":
            attrs["class"] = "language-cpp"

        attr_str = "".join([f' {k}="{v}"' for k, v in attrs.items()])
        self.output.append(f"<{tag}{attr_str}>")

        if tag == "code":
            print(self.output[-1])

    def handle_data(self, data):
        self.output.append(data)

    def handle_endtag(self, tag):
        if self.nested_level > 0:
            self.nested_level -= 1
            self.parents.pop()

        self.output.append(f"</{tag}>")


class CodeExtractor(HTMLParser):
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
            case "mark":
                self.is_mark = True
            case "pre":
                if self.is_code:
                    print(
                        f"\033[93m[WARNING] misalligned <code> and <pre> tags in lesson {self.lesson_name} line num: {self.getpos()} \033[0m"
                    )

                    if self.output[-1] == "<code>":
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
