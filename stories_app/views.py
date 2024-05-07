from django.shortcuts import render, redirect
from .models import Story
from .forms import StoryForms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def signup_page(request):
    context = {}
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            context['error'] = 'Podana nazwa użytkownika już istnieje'
            return render(request, 'login/signup.html', context)
        except User.DoesNotExist:
            if request.POST['password1'] != request.POST['password2']:
                context['error'] = 'Podane hasła są różne!'
                return render(request, 'login/signup.html', context)

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            if not first_name or not last_name:
                context['error'] = 'Imię i nazwisko są wymagane.'
                return render(request, 'login/signup.html', context)

            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'],
                    first_name=first_name,
                    last_name=last_name)
                auth.login(request, user)
                return redirect('home')
            except Exception as e:
                context['error'] = f'Wystąpił błąd podczas tworzenia konta użytkownika: {str(e)}'
                return render(request, 'login/signup.html', context)
    else:
        return render(request, 'login/signup.html', context)

def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            if request.POST.get('redir'):
                return redirect(f"{request.POST.get('redir')}")
            else:
                return redirect('home')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            if request.POST.get('redir'):
                context['next'] = 'Tylko zalogowani użytkonicy mają dostęp do tej strony!'
                context['nextURL'] = request.GET.get('next')
            return render(request, 'login/login.html', context)
    else:
        if request.GET.get('next'):
            context['next'] = 'Tylko zalogowani użytkonicy mają dostęp do tej strony!'
            context['nextURL'] = request.GET.get('next')
        return render(request, 'login/login.html', context)

def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

def home(request):
    liked_stories = Story.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:3]
    return render(request, 'home.html', {'liked_stories': liked_stories})

@login_required
def write_story(request):
    if request.method == 'POST':
        form = StoryForms(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('home')
    else:
        form = StoryForms()
    return render(request, 'write_story.html', {'form': form})

def all_stories(request):
    posts = Story.objects.all()
    return render(request, 'all_stories.html', {'posts': posts})


def story(request, item_id):
    story = Story.objects.get(pk=item_id)
    msg = False

    if request.user.is_authenticated:
        user = request.user
        if story.likes.filter(id=user.id).exists():
            msg = True

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            if story.likes.filter(id=user.id).exists():
                story.likes.remove(user)
                msg = False
            else:
                story.likes.add(user)
                msg = True

    return render(request, 'story.html', {'story': story, 'msg': msg})

def contact(request):
    return render(request, 'contact.html')