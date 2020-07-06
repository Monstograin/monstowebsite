from django.shortcuts import render,redirect
from .forms import Registration
from django.contrib.auth import login,authenticate

# Create your views here.


def register(request):
    if request.method == "POST":
        form=Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://127.0.0.1:8000')
        else:
            for msg in form.errors:
                a=form.errors[msg]
            return render(request,'register/register1.html',{"error":a})
    else:
        form=Registration()

    return render(request,'register/register1.html',{"form":form})