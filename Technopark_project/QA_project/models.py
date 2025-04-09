from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db.models import Count, Case, When, IntegerField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(null=True, default=None)
    password = models.CharField(null=True, default=None) #todo пока что чар - потом скорее всего стоит поменять
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    rating = models.IntegerField(default=0)
    user_email = models.EmailField(null=True, default=None)

    @property
    def name(self):
        return self.user.username

    def __str__(self):
        return self.name

class TagManager(models.Manager):
    def popular_tags(self):
        return self.annotate(
            num_questions=Count('question')
        ).order_by('-num_questions')[:10]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def new(self):
        # return self.order_by('-created_at')
        return self.order_by('-pk')

    def hot(self):
        return self.order_by('-rating')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)
        # return self.filter(tags__name=tag_name).order_by('-created_at')

class Question(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    text = models.TextField(validators=[MinLengthValidator(20)])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    # created_at = models.DateTimeField(auto_now_add=True, default=None)
    # edited_at = models.DateTimeField(default=None)
    rating = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)
    is_closed = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def update_rating(self):
        self.rating = QuestionLike.objects.filter(question=self, is_positive=True).count() - \
                     QuestionLike.objects.filter(question=self, is_positive=False).count()
        self.save()
    def likes(self):
        return QuestionLike.objects.filter(question=self, is_positive=True).count()
    def dislikes(self):
        return QuestionLike.objects.filter(question=self, is_positive=False).count()

class Answer(models.Model):
    text = models.TextField(validators=[MinLengthValidator(20)])
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True, default=None)
    # edited_at = models.DateTimeField(default=None)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Ответ для {self.question.title}"

    def update_rating(self):
        self.rating = AnswerLike.objects.filter(answer=self, is_positive=True).count() - \
                     AnswerLike.objects.filter(answer=self, is_positive=False).count()
        self.save()
    def likes(self):
        return AnswerLike.objects.filter(answer=self, is_positive=True).count()
    def dislikes(self):
        return AnswerLike.objects.filter(answer=self, is_positive=False).count()

class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True, default=None)

    class Meta:
        unique_together = ('question', 'user')

    def __str__(self):
        return f"{'Like' if self.is_positive else 'Dislike'} for {self.question.title}"

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f"{'Like' if self.is_positive else 'Dislike'} for answer #{self.answer.id}"