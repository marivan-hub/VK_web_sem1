from django.shortcuts import render

from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
        'popular_tags': [
            {'name': 'python'},
            {'name': 'django'},
            {'name': 'sql'},
            {'name': 'bootstrap'},
            {'name': 'javascript'},
        ],
        'best_members': [
            {'name': 'Ivanov Ivan'},
            {'name': 'Petrov Petr'},
            {'name': 'Sidorov Alex'},
        ],
    }


def index(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'Question title {i}',
            'id': i,
            'text': f'This is detailed text for question {i}. ' * 5,
            'tags': ['python', 'django', 'sql'][:i % 3 + 1],
            'answers': i % 5,
            'likes': i * 2,
            'dislikes': i % 3,
            'is_solved': i % 7 == 0,
            'is_closed': i % 5 == 0 and i % 7 != 0,
        })

    context = get_common_context()
    context['questions'] = paginate(questions, request, 5)
    return render(request, "QA_project/index.html", context)


def hot(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'Hot question  {i}',
            'id': i,
            'text': f'Текс формулировки hot вопроса {i}. ' * 5,
            'tags': ['python', 'django', 'sql'][:i % 3 + 1],
            'answers': i % 5,
            'likes': i % 10 - 5,
            'dislikes': i % 10 - 3,
            'is_solved': i % 7 == 0,
            'is_closed': i % 5 == 0 and i % 7 != 0,
        })

    context = get_common_context()
    context['questions'] = paginate(questions, request, 5)
    return render(request, "QA_project/hot.html", context)


def tag(request, tag):
    questions = []
    for i in range(1, 15):
        questions.append({
            'title': f'Вопрос по тегу {tag} {i}',
            'id': i,
            'text': f'Текст вопроса по тегу {tag} {i}. ' * 5,
            'tags': [tag, 'python', 'django'][:i % 3 + 1],
            'answers': i % 5,
            'likes': i % 10 - 5,
            'dislikes': i % 10 - 3,
            'is_solved': i % 7 == 0,
            'is_closed': i % 5 == 0 and i % 7 != 0,
        })

    context = get_common_context()
    context['questions'] = paginate(questions, request, 5)
    context['tag'] = tag
    return render(request, "QA_project/tag.html", context)



def login(request):
    return render(request,"../templates/QA_project/login.html")

def ask(request):
    return render(request,"../templates/QA_project/ask.html")

def signup(request):
    return render(request,"../templates/QA_project/signup.html")

def question(request, pk):
    answers = []
    for i in range(1, 6):
        answers.append({
            'id': i,
            'text': f'This is detailed answer {i} to question {pk}. ' * 3,
            'code': f'SELECT * FROM table_{i} WHERE id = {pk};' if i % 2 == 0 else None,
            'likes': pk * i,
            'dislikes': pk % i,
            'is_correct': i == 1,
            'author': {
                'name': f'User {i}',
                'avatar': f'resources/pictures/avatar{i % 3 + 1}.jpg'
            },
            'created_at': f'{i} day(s) ago'
        })

    question_data = {
        'title': f'Question {pk}',
        'id': pk,
        'text': 'Detailed question text. ' * 10,
        'tags': ['python', 'django', 'sql'],
        'answers': answers,
        'likes': pk * 2,
        'dislikes': pk % 3,
        'is_solved': pk % 5 == 0,
        'is_closed': False,
        'author': {
            'name': 'Question Author',
            'avatar': 'resources/pictures/avatar.jpeg'
        }
    }

    context = get_common_context()
    context['question'] = question_data
    context['answers'] = paginate(answers, request, 3)
    return render(request, "QA_project/question.html", context)


def settings(request):
    user_data = {
        'username': 'current_user',
        'email': 'user@example.com',
        'avatar': 'resources/pictures/avatar.jpeg'
    }
    context = get_common_context()
    context['user'] = user_data
    return render(request, "QA_project/settings.html", context)

def index_logout(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'Question title {i}',
            'id': i,
            'text': f'This is detailed text for question {i}. ' * 5,
            'tags': ['python', 'django', 'sql'][:i % 3 + 1],
            'answers': i % 5,
            'likes': i * 2,
            'dislikes': i % 3,
            'is_solved': i % 7 == 0,
            'is_closed': i % 5 == 0 and i % 7 != 0,
        })

    context = get_common_context()
    context['page'] = paginate(questions, request, 5)
    return render(request, "QA_project/index_logout.html", context)
