from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .form import TODOForm
from .models import TODO, Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by(
            'priority')  # use '-' sign for decending order in priority start
        return render(request, 'home.html', context={'form': form, 'todos': todos})

def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form": form1
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                messages.success(request, 'Login successfully')
                return redirect('home')
        else:
            context = {
                "form": form
            }
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', context=context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwoed = request.POST.get('password')

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is already taken.')
                return redirect('/signup')

            if User.objects.filter(email=email).first():
                messages.error(request, 'email is already taken.')
                return redirect('/signup')

            user_obj = User(username=username, email=email)
            user_obj.set_password(passwoed)
            user_obj.save()
            messages.success(request, "Your TODO account has been created successfully")
        except Exception as e:
            print(e)
    return render(request, 'signup.html')

@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            messages.success(request, 'Your Todo added successfully')
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})


def signout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('login')


def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    messages.success(request, 'Todo deleted Successfully')
    return redirect('home')


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    messages.success(request, "Todo Change successfully")
    return redirect('home')



