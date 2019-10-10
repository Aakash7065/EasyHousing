from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contacts


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "logged in successfully")
            return redirect('dashboard')
        else:
            messages.error('invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            assert password == password2, "Password do not match"
            assert not User.objects.filter(username=username).exists(), "User Already Exists"
            assert not User.objects.filter(email=email).exists(), "Email Already Exists"
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            # auth.login(request, user)
            # messages.success(request, "you are now logged in")
            # redirect('index')
            user.save()
            messages.success(request, "registered successfully, can login")
            return redirect('login')
        except AssertionError as e:
            messages.error(request, ''.join(e.args))
            return redirect('register')
    return render(request, 'accounts/signup.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "you are now logout")
        return redirect('index')
    return redirect('index')


def dashboard(request):
    contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': contacts
    }
    return render(request, 'accounts/dashboard.html',context)
