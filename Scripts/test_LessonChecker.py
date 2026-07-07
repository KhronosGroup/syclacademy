import argparse
import unittest
import LessonChecker

class TestSYCLAParser(unittest.TestCase):
    pass

test_cases = [
    {
        "name": "detect_swapped_code_pre",
        "body": "<code><pre></code></pre>",
        "extract": False,
        "verify": True,
        "fix": False,
        "expected_return": True,
    },
    {
        "name": "detect_illegal_tag_in_code",
        "body": "<pre><code><span></code></pre>",
        "extract": False,
        "verify": True,
        "fix": False,
        "expected_return": True,
    },
    {
        "name": "detect_mark_in_code",
        "body": "<pre><code><mark>message</mark></code><pre>",
        "extract": False,
        "verify": True,
        "fix": False,
        "expected_return": False,
    },
    {
        "name": "parse_start_end_tag",
        "body": "<div><img /></div>",
        "extract": True,
        "verify": True,
        "fix": False,
        "expected_return": False,
    },
    {
        "name": "parse_self_closing_tag",
        "body": "<html><head><link></link></head><html>",
        "extract": True,
        "verify": True,
        "fix": False,
        "expected_return": True,
    },
    {
        "name": "validate_comment",
        "body": "<!--comment--><div><p>content</p></div>",
        "extract": False,
        "verify": True,
        "fix": False,
        "expected_return": False,
    },
    {
        "name": "validate_decl",
        "body": "<!DOCTYPE html>",
        "extract": False,
        "verify": True,
        "fix": False,
        "expected_return": False,
    },
    {
        "name": "extract_code_block",
        "body": "<pre><code>int main() { return 0; }</code></pre>",
        "extract": True,
        "verify": False,
        "fix": False,
        "expected_return": False,
        "expected_code": "int main() { return 0; }",
    },
    {
        "name": "extract_entity_ref_in_code_block",
        "body": "<pre><code>&evt</code></pre>",
        "extract": True,
        "verify": False,
        "fix": False,
        "expected_return": True,
        "expected_code": "&evt",
    },
    {
        "name": "extract_proper_lt_and_gt",
        "body": "<pre><code>#include&lt;sycl/sycl.hpp&gt;</code></pre>",
        "extract": True,
        "verify": False,
        "fix": False,
        "expected_return": False,
        "expected_code": "#include<sycl/sycl.hpp>",
    },
    {
        "name": "fix_mismatched_pre_code",
        "body": "<code><pre></code></pre>", 
        "extract": False,
        "verify": False,
        "fix": True,
        "expected_return": True,
        "expected_output": '<pre><code class="language-cpp"></code></pre>',
    },
    {
        "name": "fix_improper_escaped_ref",
        "body": '<pre><code class="language-cpp">&evt</code></pre>',
        "extract": False,
        "verify": False,
        "fix": True,
        "expected_return": True,
        "expected_output": '<pre><code class="language-cpp">&amp;evt</code></pre>',
    },
    {
        "name": "fix_improper_escaped_gators",
        "body": '<pre><code class="language-cpp">#include<sycl/sycl.hpp></code></pre>',
        "extract": False,
        "verify": False,
        "fix": True,
        "expected_return": True,
        "expected_output": '<pre><code class="language-cpp">#include&lt;sycl/sycl.hpp&gt;</code></pre>',
    }
]

def make_test_method(case_data):
    def test_method(self):
        args = argparse.Namespace(
            extract=case_data["extract"],
            verify=case_data["verify"],
            fix=case_data["fix"]
        )
        
        output, code, error = LessonChecker.verify_html(
            lesson="test_lesson", 
            file_str=case_data["body"], 
            args=args
        )
        
        self.assertEqual(error, case_data["expected_return"])
        
        if case_data["extract"] and "expected_code" in case_data:
            self.assertEqual(code[0][1], case_data["expected_code"])
            
        if case_data["fix"] and "expected_output" in case_data:
            self.assertEqual(output, case_data["expected_output"])
        
    return test_method

for case in test_cases:
    test_method_name = f"test_{case['name']}"
    setattr(TestSYCLAParser, test_method_name, make_test_method(case))

