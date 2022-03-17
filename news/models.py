from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) #cвязь «один к одному» с встроенной моделью пользователей User;
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating_post'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating_comment'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, )

    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    News = 'NW'
    Article = 'AR'

    CATEGORY_CHOICES = [
        (News, 'Новость'),
        (Article, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE) #связь «один ко многим» с моделью Author;
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=Article)
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True) #связь «многие ко многим» с моделью Category
    title = models.CharField(max_length=228)
    text = models.TextField()
    rating_post = models.SmallIntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'pk': self.id})


#class PostCategory(models.Model):
#    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE) #связь «один ко многим» с моделью Post;
#    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE) #связь «один ко многим» с моделью Category;



class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE) #связь «один ко многим» с моделью Post;
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE) #связь «один ко многим» со встроенной моделью User;
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating_comment = models.SmallIntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

