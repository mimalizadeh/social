from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from account.forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], password=cd['password1'], email=cd['email'])
            messages.success(request, "User registered successfully", extra_tags='success')
            return redirect('home:home')

        return render(request, 'account/register.html', {'form': form})


class UserLoginView(View):
    from_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.from_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.from_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request=request, user=user)
                messages.success(request, "User logged in successfully", extra_tags='success')
                return redirect("home:home")
            else:
                messages.error(request, "Username or password is wrong ", extra_tags="danger")
                return redirect("home:home")

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out successfully')
        return redirect('home:home')

    def post(self, request):
        pass
