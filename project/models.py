from django.db import models
import uuid  # for overrding id to 16 bit
# one to many relation project(owner) and profile
from users.models import Profile

# Create your models here.


class Project(models.Model):  # models.Model tell that this class should now take as model
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # required parameter max_length
    # null = True if desc is emplty it is added to database (for database) blank=true is for django
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # 'Tag' in '' coz it is defined below so it makes it lazy
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # enter current time means when instance is created
    created = models.DateTimeField(auto_now_add=True)
    # overridding django defautl id
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        # what if two project have same vote ratio
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list(
            'owner__id', flat=True)  # flat=True make it list #getting owner id who have reviewed project
        return queryset

    @property  # so we can use it as attribute not as method
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)  # one to many
    # on_delete=models.CASCADE when project deleted reviews will also get deleted
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(
        max_length=200, choices=VOTE_TYPE)  # upvote or downvote
    # enter current time means when instance is created
    created = models.DateTimeField(auto_now_add=True)
    # overridding django defautl id
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        # binding owner and project so one owner can comments one project
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    # enter current time means when instance is created
    created = models.DateTimeField(auto_now_add=True)
    # overridding django defautl id
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
