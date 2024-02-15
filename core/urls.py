from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(views.TaskListView.as_view()),name="task"),
    path('task/<int:pk>/',login_required(views.TaskDetailView.as_view()),name='task_detail'),
    path('addtask/',views.TaskCreateView.as_view(),name='addtask'),
    path('updatetask/<int:pk>/',views.TaskUpdateView.as_view(),name='updatetask'),
    path('deletetask/<int:pk>/',views.TaskDeleteView.as_view(),name='deletetask'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('signup/',views.UserSignUpView.as_view(),name='signup'),
]