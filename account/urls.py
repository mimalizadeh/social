from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('edit_profile/',views.UserEditProfile.as_view(),name = 'edit_profile'),

    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done', views.UserPasswordResetDoneView.as_view(), name='reset_password_done'),
    path('confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='reset_password_complete'),

    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user_unfollow'),

]
