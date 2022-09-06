from django.shortcuts import render, redirect

default_welcome_code = """#include<iostream>
using namespace std;
int main() {
    
}
"""
default_evaluate_code = """#include<iostream>
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


# Create your views here.
def welcome(request):
    if request.method == "POST":
        code = request.POST.get("code", default_welcome_code)
        print("code", code)
        compiled = request.POST.get("compiled", None)
        if compiled is None:
            compiled = parse_code(code)
        context = {
            "code": code,
            "compiled": compiled,
        }
        return render(request, "index.html", context=context)
    return render(request, "index.html")


def parse_code(code):
    return 1


def evaluation_service(request):
    if request.method != "POST":
        return redirect("/")
    code = request.POST.get("code", default_welcome_code)
    compiled = parse_code(code)
    if compiled != 1:
        return redirect("/")

    code = default_evaluate_code + "\nAbove is an example code. Here is the code that you compiled:\n" + code

    lines = [
        "for" if "for" in line else "main" if "main" in line else "if" if "if" in line else "int" if "int" in line else "other"
        for line in code.split("\n")
    ]
    context = {
        "code": code,
        "lines": lines
    }
    return render(request, "evaluate.html", context=context)
