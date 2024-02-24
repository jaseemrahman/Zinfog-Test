from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
    # Login
    path('',views.LoginPageView.as_view(),name='login'),
    # Logout
    path('Logout',views.Logout.as_view(),name='logout'),

    # Student
    path('Student-Registration',views.StudentRegistrationPageView.as_view(),name='StudentRegistration'),
    path('Student-Dashboard',views.StudentDashboard.as_view(),name='student-dashboard'),
    path('Student-Profile-Edit',views.StudentProfileEditView.as_view(),name='student-profile'),

    # Admin
    path('Admin-Registration',views.AdminRegistrationPageView.as_view(),name='AdminRegistration'),
    path('Admin-Dashboard',views.AdminDashboard.as_view(),name='AdminList'),

]
