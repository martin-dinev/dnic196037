from django.shortcuts import render, redirect

from analyzer.compiler import parse_code

default_welcome_code = """#include <iostream>
using namespace std;
int main() {
    
}
"""
default_evaluate_code = """#include <iostream>
using namespace std;
int main() {
    int x = 16, y, z=123;
    if(x>12)
        x=12;
    int sum = 0;
    for(int i = 1 ; i <= 5 ; i ++){
        sum += x*(i+2) - x/2;
        x -= 2;
    }
}
"""


class LOGIC:
    def __init__(self, compiled, message, executable=None):
        self.compiled = compiled
        self.message = message
        self.executable = executable
    def get_compile_button_class(self):
        return "btn " + ("btn-light" if self.compiled is None else ("btn-success" if self.compiled else "btn-warning"))

    def get_evaluate_button_class(self):
        return "btn " + ("btn-primary" if self.compiled else "btn-danger disabled")

    @staticmethod
    def get_default_code():
        return default_welcome_code


def welcome(request):
    if request.method == "POST":
        code = request.POST.get("code", default_welcome_code)
        message = None
        runnable = None
        compiled, message, runnable = parse_code(code)
        context = {
            "code": code,
            "logic": LOGIC(compiled, message, runnable)
        }
        return render(request, "index.html", context=context)
    return render(request, "index.html", context={"logic": LOGIC(None, None)})


def evaluation_service(request):
    if request.method != "POST":
        return redirect("/")
    code = request.POST.get("code", default_welcome_code)
    compiled, message, runnable = parse_code(code)
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
