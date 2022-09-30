from itertools import takewhile

from django.shortcuts import render, redirect

default_welcome_code = """#include <iostream>
using namespace std;
int main() {
    
}
"""
default_evaluate_code = """#include <iostream>
using namespace std;
int main() {
    int x = 16;
    if(x>12)
        x=12;
    int sum = 0;
    for(int i = 1 ; i <= 5 ; i ++){
        sum += x*i - x/2;
        x -= 2;
    }
}
"""


class LOGIC:
    def __init__(self, compiled, message):
        self.compiled = compiled
        self.message = message

    def get_compile_button_class(self):
        return "btn " + ("btn-light" if self.compiled is None else ("btn-success" if self.compiled else "btn-warning"))

    def get_evaluate_button_class(self):
        return "btn " + ("btn-primary" if self.compiled else "btn-danger disabled")

    @staticmethod
    def get_default_code():
        return default_welcome_code


# Create your views here.
def welcome(request):
    if request.method == "POST":
        code = request.POST.get("code", default_welcome_code)
        compiled = request.POST.get("compiled", None)
        message = None
        if compiled is None:
            compiled, message = parse_code(code)
        context = {
            "code": code,
            "logic": LOGIC(compiled, message)
        }
        return render(request, "index.html", context=context)
    return render(request, "index.html", context={"logic": LOGIC(None, None)})


def evaluation_service(request):
    if request.method != "POST":
        return redirect("/")
    code = request.POST.get("code", default_welcome_code)
    compiled, message = parse_code(code)
    if not compiled:
        return redirect("/")

    code = default_evaluate_code + "\n//Above is an example code. Here is the code that you compiled:\n" + code

    lines = [
        "for" if "for" in line else "main" if "main" in line else "if" if "if" in line else "int" if "int" in line else "other"
        for line in code.split("\n")
    ]
    context = {
        "code": code,
        "lines": lines
    }
    return render(request, "evaluate.html", context=context)


def parse_code(code):  # returns (success, runnable) where success -> runnable: True -> runnable; False -> message
    success, tokens_or_message = tokenize(code)
    if not success:
        message = tokens_or_message
        return False, message
    tokens = tokens_or_message

    if tokens[0] != "#include <iostream>":
        return False, "first line must be '#include <iostream>'"
    if tokens[1:5] != ["using", "namespace", "std", ";"]:
        return False, "second line must be 'using namespace std;'"
    if tokens[5:9] != ["int", "main", "(", ")"]:
        return False, "third line must be 'int main()'"
    if tokens[9] != "{":
        return False, "'int main()' must be followed by '{'"

    variable_names = set()
    scope_stack = []
    pos = 9

    def compile_scope():
        nonlocal pos
        pos = len(tokens)
        return ""

    result = compile_scope()
    if pos != len(tokens):
        return False, "there must not be code out of main scope"
    return True, result


BRACKETS = {"{": "}", "(": ")"}
MULTI_CHARS_OPERATORS = ("++", "<=", ">=", "+=", "-=")
SINGLE_CHAR_OPERATORS = ("-", ">", "<", ";", "*", "/", "=")


def next_token(code):
    once = False
    while not once or (len(code) > 0 and code[0] == '\n'):
        once = True
        if len(code) > 0 and code[0] == "\n":
            code = code[1:]
        code = code.lstrip()

    if len(code) == 0:
        return True, None

    if code[0].isalpha():
        return True, "".join(takewhile(lambda ch: ch.isalnum() or ch == "_", code))

    if code[0].isnumeric():
        return True, "".join(takewhile(lambda ch: ch.isnumeric(), code))

    if code[0] == "#":
        incl = "#include <iostream>"
        if code[:len(incl)] == incl:
            return True, "#include <iostream>"
        else:
            return False, "# can only include iostream"

    if code[:2] in MULTI_CHARS_OPERATORS:
        return True, code[:2]

    if code[0] in SINGLE_CHAR_OPERATORS:
        return True, code[0]

    if code[0] in BRACKETS.keys():
        count = 1
        pos = 1
        while count > 0:
            new_pos_open = code.find(code[0], pos)
            new_pos_close = code.find(BRACKETS[code[0]], pos)
            if new_pos_open != -1 and new_pos_open < new_pos_close:
                count += 1
                pos = new_pos_open + 1
            elif new_pos_close == -1:
                return -1, code[0] + " missing a closing bracket"
            else:
                count -= 1
                pos = new_pos_close + 1
        return True, code[0]

    if code[0] in BRACKETS.values():
        return True, code[0]

    return False, "I have never seen " + code[0]


def tokenize(code):
    tokens = []
    while True:
        success, token_or_message = next_token(code)
        if success:
            token = token_or_message
            if token is None:
                break
            tokens.append(token)
            code = code[code.index(token) + len(token):]
        else:
            message = token_or_message
            return False, message
    return True, tokens
