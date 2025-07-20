from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import GreenIdea, Category
from .forms import CustomUserCreationForm, GreenIdeaForm
from django.db.models import Q
from django.contrib.auth import logout as auth_logout

class IndexView(ListView):
    model = GreenIdea
    template_name = 'green_app/index.html'
    context_object_name = 'ideas'
    ordering = ['-submission_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            num_visits = self.request.session.get('num_visits', 0)
            self.request.session['num_visits'] = num_visits + 1
            context['num_visits'] = num_visits + 1
        context['categories'] = Category.objects.all()
        return context

class IdeaDetailView(DetailView):
    model = GreenIdea
    template_name = 'green_app/idea_detail.html'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'green_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'green_app/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('index')

class SubmitIdeaView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = GreenIdeaForm()
        return render(request, 'green_app/submit_idea.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = GreenIdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.submitted_by = request.user
            idea.save()
            return redirect('idea_detail', pk=idea.pk)
        return render(request, 'green_app/submit_idea.html', {'form': form})

def search_view(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    results = GreenIdea.objects.all().order_by('-submission_date')

    if query:
        results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if category_id:
        results = results.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'green_app/search_results.html', {
        'results': results,
        'query': query or "all",
        'categories': categories
    })

def about_us_view(request):
    return render(request, 'green_app/about_us.html')
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def unregister_view(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('index')  # or a 'goodbye' page
    return render(request, 'green_app/unregister_confirm.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import GreenIdea

@login_required
def delete_idea_view(request, pk):
    idea = get_object_or_404(GreenIdea, pk=pk)
    if request.user == idea.submitted_by or request.user.is_superuser:
        if request.method == 'POST':
            idea.delete()
            return redirect('index')
        return render(request, 'green_app/delete_idea_confirm.html', {'idea': idea})
    return HttpResponseForbidden("You are not allowed to delete this idea.")


from .models import GreenIdea
from django.utils.timezone import now

class IndexView(ListView):
    model = GreenIdea
    template_name = 'green_app/index.html'
    context_object_name = 'ideas'
    ordering = ['-submission_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            num_visits = self.request.session.get('num_visits', 0)
            self.request.session['num_visits'] = num_visits + 1
            self.request.session['last_visit'] = self.request.session.get('last_visit') or str(now())
            context['num_visits'] = num_visits + 1
            context['last_visit'] = self.request.session['last_visit']
        context['categories'] = Category.objects.all()
        return context
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def user_history_view(request):
    num_visits = request.session.get('num_visits', 0)
    last_visit = request.session.get('last_visit', 'First visit this session')

    # Update for next time
    request.session['num_visits'] = num_visits + 1
    request.session['last_visit'] = now().strftime('%Y-%m-%d %H:%M:%S')

    context = {
        'num_visits': num_visits + 1,
        'last_visit': last_visit
    }
    return render(request, 'green_app/user_history.html', context)
