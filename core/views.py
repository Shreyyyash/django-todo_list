from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from .models import Tasks
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from datetime import date ,datetime

# Create your views here.

class TaskListView(ListView):
    model=Tasks
    template_name='core/task_list.html'
    ordering='completion'
    context_object_name= 'tasks_list'
    paginate_by= 3
    # paginate_orphans=1
    today = datetime.now()
    month = today.strftime('%B')
    day=today.strftime("%A")
    date=today.today().strftime('%d')
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset().filter(user=self.request.user)
        # Get the search term from the search bar
        search_task = self.request.GET.get('search-task') or ''
        if search_task:
            queryset = queryset.filter(title__icontains=search_task)
        
        queryset = queryset.order_by('completion', '-created')
        return queryset

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        # Fetch all tasks for the user
        tasks_list = self.get_queryset()

        # Paginate the tasks
        paginator = self.get_paginator(tasks_list, self.paginate_by)
        page = self.request.GET.get('page',1)

        try:
            tasks_list = paginator.page(page)
        except Exception as e: 
            tasks_list = paginator.page(1)

        context['tasks_list'] = tasks_list
        # context['count'] = tasks_list.object_list.filter(completion=False).count()
        context['count'] = Tasks.objects.filter(user=self.request.user,completion=False).count()
        context['month'] = self.month
        context['day'] = self.day
        context['date'] = self.date

        # Pass search_task to the template
        context['searchingtask'] = self.request.GET.get('search-task', '')

        return context
    
class TaskDetailView(DetailView):
    model=Tasks
    template_name='core/task_detail.html'

class TaskCreateView(LoginRequiredMixin,CreateView):
    model=Tasks
    template_name='core/task_form.html'
    fields=['title','description','completion']
    success_url='/'

    # to save the form / add task
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model=Tasks
    template_name='core/task_update.html'
    fields=['title','description','completion']
    success_url='/'

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model=Tasks
    # template_name='core/task_delete.html'
    success_url='/'
    
class UserLoginView(LoginView):
    template_name='core/login.html'
    redirect_authenticated_user=True
    
    def get_success_url(self) -> str:
        return reverse_lazy('task')

class UserLogoutView(LogoutView):
    next_page='login'

class UserSignUpView(SuccessMessageMixin,CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'core/signup.html'
    success_message='Account created successfully.'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('/')
        return super().get(request, *args, **kwargs)

