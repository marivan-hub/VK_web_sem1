from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"../templates/QA_project/index.html")

def login(request):
    return render(request,"../templates/QA_project/login.html")

def ask(request):
    return render(request,"../templates/QA_project/ask.html")

def signup(request):
    return render(request,"../templates/QA_project/signup.html")

def question(request):
    return render(request,"../templates/QA_project/question.html")

def settings(request):
    return render(request,"../templates/QA_project/settings.html")