from django.shortcuts import render,redirect
from .forms import Registration
from django.contrib.auth import login,authenticate

# Create your views here.


def register(request):
    if request.method == "POST":
        form=Registration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin')
        else:
            for msg in form.errors:
                a=form.errors[msg]
            return render(request,'register/register.html',{"error":a})
    else:
        form=Registration()

    return render(request,'register/register.html',{"form":form})