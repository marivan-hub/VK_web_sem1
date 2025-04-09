from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Question, Tag, Profile, Answer

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
        # 'popular_tags': Tag.objects.popular_tags(),
        'popular_tags': Tag.objects.all(),
        # 'best_members': Profile.objects.best_members(),
        'best_members': Profile.objects.all()[:10],
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
    answers = Answer.objects.filter(question=question).order_by('-is_correct', '-rating')
    context = get_common_context()
    context['question'] = question
    context['page'] = paginate(answers, request, per_page=5)
    return render(request, "QA_project/question.html", context)


def ask(request):
    context = get_common_context()
    return render(request, "QA_project/ask.html", context)


def login(request):
    context = get_common_context()
    return render(request, "QA_project/login.html", context)


def signup(request):
    context = get_common_context()
    return render(request, "QA_project/signup.html", context)


def settings(request):
    context = get_common_context()
    context['user'] = request.user.profile
    return render(request, "QA_project/settings.html", context)


def index_logout(request):
    questions = Question.objects.new()
    context = get_common_context()
    context['page'] = paginate(questions, request)
    return render(request, "QA_project/index_logout.html", context)