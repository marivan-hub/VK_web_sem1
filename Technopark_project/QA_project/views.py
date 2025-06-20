from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from .forms import AskForm, AnswerForm
from .forms import SignupForm, LoginForm, ProfileEditForm
from .models import Question, Tag, Profile, Answer
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def get_common_context():
    return {
        'popular_tags': Tag.objects.popular_tags(),
        'best_members': Profile.objects.best_members(),
    }


def index(request):
    questions = Question.objects.new()
    context = get_common_context()
    context['page'] = paginate(questions, request)
    return render(request, "QA_project/index.html", context)


def hot(request):
    questions = Question.objects.hot()
    context = get_common_context()
    context['page'] = paginate(questions, request)
    return render(request, "QA_project/hot.html", context)


def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request)  #
    context = get_common_context()
    context['page'] = page  #
    context['tag'] = tag_obj
    return render(request, "QA_project/tag.html", context)


def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers_qs = Answer.objects.filter(question=question).order_by('-is_correct', '-rating')

    context = get_common_context()
    context['question'] = question

    per_page = 5
    paginator = Paginator(answers_qs, per_page)
    page_number = 1
    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = reverse('login') + '?continue=' + request.path
            return redirect(login_url)

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = question
            answer.save()
            question.answers_count = question.answers.count()
            question.save()
            all_answers = list(answers_qs)
            answer_index = all_answers.index(answer)

            page_number = answer_index // per_page + 1

            url = reverse('question', kwargs={'pk': pk}) + f'?page={page_number}#answer-{answer.id}'
            return redirect(url)
    else:
        page_number = request.GET.get('page', 1)

    page = paginator.get_page(page_number)
    context['page'] = page
    context['form'] = form if request.method == 'POST' else AnswerForm()

    return render(request, "QA_project/question.html", context)



@login_required
def ask(request):
    context = get_common_context()
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(author=request.user.profile)
            return redirect('question', pk=question.pk)
    else:
        form = AskForm()
    context['form'] = form
    return render(request, "QA_project/ask.html", context)


def login_view(request):
    next_url = request.GET.get('continue', request.POST.get('continue', '/'))
    context = get_common_context()
    context['form'] = LoginForm(request.POST or None)
    context['continue'] = next_url
    if request.method == 'POST' and context['form'].is_valid():
        user = authenticate(
            request,
            username=context['form'].cleaned_data['username'],
            password=context['form'].cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('index')
        else:
            context['form'].add_error(None, 'Invalid username or password')

    return render(request, 'QA_project/login.html', context)




def signup(request):
    context = get_common_context()
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    context['form'] = form
    return render(request, "QA_project/signup.html", context)

@login_required
def settings(request):
    context = get_common_context()
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ProfileEditForm(instance=profile)
    context['form'] = form
    return render(request, "QA_project/settings.html", context)


def logout_view(request):
    referer = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return redirect(referer)