from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from account.forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from account.models import Relation


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next = None

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')

        return super().dispatch(request, *args, **kwargs)

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
                if self.next is not None:
                    return redirect(self.next)
                return redirect("home:home")
            else:
                messages.error(request, "Username or password is wrong ", extra_tags="danger")
                return redirect("home:home")

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out successfully')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        is_followed = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user.id)
        if relation.exists():
            is_followed = True

        return render(request, 'account/profile.html', {'user': user, 'posts': posts, 'is_followed': is_followed})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:reset_password_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:reset_password_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You already followed this user ', extra_tags='danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'You followed this user', extra_tags='success')

        return redirect("account:user_profile", user_id)


class UserUnfollowView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'You unfollowed this user', extra_tags='success')
        else:
            messages.error(request, 'You not followed this user')

        return redirect('account:user_profile', user_id)
