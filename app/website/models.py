from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField
from taggit.managers import TaggableManager


class ContactMessage(models.Model):
    """
    Model for contact messages
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField()
    notified = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class Product(models.Model):
    """
    Model for products
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='products/thumbnails/',
                                  force_format='JPEG', quality=75)
    banner = ResizedImageField(size=[1280, 720], crop=['middle', 'center'], upload_to='products/banners/',
                               force_format='JPEG', quality=75)
    name = models.CharField(max_length=100)
    description = RichTextUploadingField()
    tags = TaggableManager()

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class ProductAdvantage(models.Model):
    """
    Model for product advantages
    """

    advantage = models.CharField(max_length=100)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='advantages')

    def __str__(self):
        """
        Returns the advantage
        """

        return self.advantage


class ProductDisadvantage(models.Model):
    """
    Model for product disadvantages
    """

    disadvantage = models.CharField(max_length=100)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='disadvantages')

    def __str__(self):
        """
        Returns the disadvantage
        """

        return self.disadvantage


class Project(models.Model):
    """
    Model for projects
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='posts/thumbnails/',
                                  force_format='JPEG', quality=75)
    name = models.CharField(max_length=100)
    construction_date = models.DateField()
    products = models.ManyToManyField('Product', related_name='projects')
    colors = models.ManyToManyField('Color', related_name='colors')
    city = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class ProjectPicture(models.Model):
    """
    Model for project pictures
    """

    picture = ResizedImageField(size=[750, 500], crop=['middle', 'center'], upload_to='posts/banners/',
                                force_format='JPEG', quality=75)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pictures')


class Color(models.Model):
    """
    Model for colors
    """

    name = models.CharField(max_length=100)
    hex = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class Post(models.Model):
    """
    Model for posts
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='posts/thumbnails/',
                                  force_format='JPEG', quality=75)
    banner = ResizedImageField(size=[1280, 720], crop=['middle', 'center'], upload_to='posts/banners/',
                               force_format='JPEG', quality=75)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    date = models.DateField()
    tags = TaggableManager()

    def __str__(self):
        """
        Returns the title
        """

        return self.title


class QAndA(models.Model):
    """
    Model for Q&A
    """

    question = models.CharField(max_length=100)
    answer = RichTextUploadingField()

    def __str__(self):
        """
        Returns the question
        """

        return self.question
