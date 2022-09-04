from django.shortcuts import render

# Create your views here.
def welcome(request):
    if request.method == "POST":
        code = request.POST.get("code", ":(")
        print(code)
        return render(request, "index.html", context={"code":code+'\n'+code})
    return render(request,"index.html")