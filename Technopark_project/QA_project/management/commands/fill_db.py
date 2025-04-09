from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random
from QA_project.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

fake = Faker()


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']

        users = []
        for _ in range(ratio):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.email(),
                password='testpass123'
            )
            profile = Profile.objects.create(user=user)
            users.append(profile)

        tags = []
        for _ in range(ratio):
            tag = Tag.objects.create(
                name=fake.unique.word(),
                description=fake.sentence()
            )
            tags.append(tag)

        questions = []
        for _ in range(ratio * 10):
            question = Question.objects.create(
                title=fake.sentence()[:-1] + '?',
                text='\n'.join(fake.paragraphs()),
                author=random.choice(users),
                rating=random.randint(-10, 50),
                answers_count=random.randint(0, 20),
                is_closed=random.random() < 0.1,
                is_solved=random.random() < 0.05
            )
            question.tags.set(random.sample(tags, min(3, len(tags))))
            questions.append(question)

        answers = []
        for _ in range(ratio * 100):
            answer = Answer.objects.create(
                text='\n'.join(fake.paragraphs()),
                question=random.choice(questions),
                author=random.choice(users),
                rating=random.randint(-5, 30),
                is_correct=random.random() < 0.1
            )
            answers.append(answer)

        for _ in range(ratio * 200):
            question = random.choice(questions)
            user = random.choice(users)

            if not QuestionLike.objects.filter(question=question, user=user).exists():
                QuestionLike.objects.create(
                    question=question,
                    user=user,
                    is_positive=random.random() < 0.8
                )
                question.update_rating()

        for _ in range(ratio * 200):
            answer = random.choice(answers)
            user = random.choice(users)

            if not AnswerLike.objects.filter(answer=answer, user=user).exists():
                AnswerLike.objects.create(
                    answer=answer,
                    user=user,
                    is_positive=random.random() < 0.8
                )
                answer.update_rating()

        self.stdout.write(self.style.SUCCESS(f'Successfully filled database with ratio {ratio}'))