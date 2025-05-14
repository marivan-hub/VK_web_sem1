import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import now
from QA_project.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.db import transaction
from faker import Faker

fake = Faker()

BATCH_SIZE = 10000


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Fill ratio')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(self.style.WARNING('Starting database fill...'))

        with transaction.atomic():
            self._create_users(num_users)
            self._create_tags(num_tags)
            self._create_questions(num_questions)
            self._create_answers(num_answers)
            self._create_likes(num_likes)

        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))

    def _create_users(self, num_users):
        self.stdout.write(f'Creating {num_users} users...')
        users = [
            User(username=f"user_{i}", email=f"user_{i}@example.com")
            for i in range(num_users)
        ]
        User.objects.bulk_create(users, batch_size=BATCH_SIZE)
        user_ids = list(User.objects.order_by('-id').values_list('id', flat=True)[:num_users])
        profiles = [
            Profile(user_id=uid, nickname=fake.first_name(), user_email=f"user_{i}@example.com")
            for i, uid in enumerate(user_ids)
        ]
        Profile.objects.bulk_create(profiles, batch_size=BATCH_SIZE)

    def _create_tags(self, num_tags):
        self.stdout.write(f'Creating {num_tags} tags...')
        tags = [
            Tag(name=f"tag_{i}", description=fake.sentence())
            for i in range(num_tags)
        ]
        Tag.objects.bulk_create(tags, batch_size=BATCH_SIZE)

    def _create_questions(self, num_questions):
        self.stdout.write(f'Creating {num_questions} questions...')
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        tag_ids = list(Tag.objects.values_list('id', flat=True))

        questions = [
            Question(
                title=fake.sentence(nb_words=6),
                text=fake.paragraph(nb_sentences=3),
                author_id=random.choice(profile_ids),
                edited_at=now()
            ) for _ in range(num_questions)
        ]
        Question.objects.bulk_create(questions, batch_size=BATCH_SIZE)

        questions = list(Question.objects.order_by('-id')[:num_questions])
        through_model = Question.tags.through
        m2m_relations = set()

        for question in questions:
            num_tags_for_question = random.randint(1, 3)
            selected_tags = random.sample(tag_ids, k=min(num_tags_for_question, len(tag_ids)))
            for tag_id in selected_tags:
                m2m_relations.add((question.id, tag_id))

        through_model_objs = [
            through_model(question_id=q_id, tag_id=tag_id)
            for q_id, tag_id in m2m_relations
        ]

        through_model.objects.bulk_create(through_model_objs, batch_size=BATCH_SIZE)

    def _create_answers(self, num_answers):
        self.stdout.write(f'Creating {num_answers} answers...')
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))

        answers = [
            Answer(
                text=fake.paragraph(nb_sentences=2),
                question_id=random.choice(question_ids),
                author_id=random.choice(profile_ids),
                edited_at=now()
            ) for _ in range(num_answers)
        ]
        Answer.objects.bulk_create(answers, batch_size=BATCH_SIZE)

    def _create_likes(self, num_likes):
        self.stdout.write(f'Creating {num_likes} question and answer likes...')
        profile_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))
        answer_ids = list(Answer.objects.values_list('id', flat=True))

        qlikes = set()
        alikes = set()

        while len(qlikes) < num_likes // 2:
            qlikes.add((random.choice(question_ids), random.choice(profile_ids)))
        while len(alikes) < num_likes // 2:
            alikes.add((random.choice(answer_ids), random.choice(profile_ids)))

        qlikes_objs = [
            QuestionLike(
                question_id=qid,
                user_id=uid,
                is_positive=random.choice([True, False])
            ) for qid, uid in qlikes
        ]
        alikes_objs = [
            AnswerLike(
                answer_id=aid,
                user_id=uid,
                is_positive=random.choice([True, False])
            ) for aid, uid in alikes
        ]
        if qlikes_objs:
            QuestionLike.objects.bulk_create(qlikes_objs, batch_size=BATCH_SIZE, ignore_conflicts=True)
        if alikes_objs:
            AnswerLike.objects.bulk_create(alikes_objs, batch_size=BATCH_SIZE, ignore_conflicts=True)
