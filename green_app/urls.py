from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('idea/<int:pk>/', views.IdeaDetailView.as_view(), name='idea_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('submit/', views.SubmitIdeaView.as_view(), name='submit_idea'),
    path('search/', views.search_view, name='search'),
    path('about/', views.about_us_view, name='about_us'),
    path('unregister/', views.unregister_view, name='unregister'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('idea/<int:pk>/delete/', views.delete_idea_view, name='delete_idea'),
path('history/', views.user_history_view, name='user_history'),

]