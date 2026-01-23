from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from adminapp.models import Customer


# Create your views here.
@never_cache
def login_page(request):
    User=get_user_model()
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username = username,password=password)
        if user and user.is_active:
            login(request,user)
            return redirect('home')
        else:
            print(messages)
            messages.error(request,"Invalid username or password!!")
            return redirect('login')
    return render(request, 'user/login.html')

def signup_page(request):
    User = get_user_model()

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 🧠 Password match validation
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # 🔍 Unique username & email validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        # ✅ Create the new user
        user = User.objects.create_user(
            username=username,
            password=password1,
            first_name=fname,
            last_name=lname,
            email=email
        )

        # ✅ Create linked Customer profile (no email field now)
        Customer.objects.create(
            user=user,
            status='Active'
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')
    return render(request, 'user/signup.html')

@never_cache
def logout_page(request):
    logout(request)
    return redirect('login')

@never_cache
def forgotpassword_page(request):
    User = get_user_model()

    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        #  Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('forgotpassword')

        #  Check user existence
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username!")
            return redirect('forgotpassword')

        # Set hashed password
        user.set_password(password1)
        user.save()

        messages.success(request, "Password reset successfully! Please login.")
        return redirect('login')

    return render(request, 'user/forgotpassword.html')
