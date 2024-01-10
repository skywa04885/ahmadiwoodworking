from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django_resized import ResizedImageField
from meta.models import ModelMeta
from django.urls import reverse


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


class Product(ModelMeta, models.Model):
    """
    Model for products
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='products/thumbnails/',
                                  force_format='WEBP', quality=75)
    banner = ResizedImageField(size=[1280, 720], crop=['middle', 'center'], upload_to='products/banners/',
                               force_format='WEBP', quality=75)
    name = models.CharField(max_length=100)
    description = RichTextUploadingField()

    # The metadata.
    _metadata = {
        'title': 'name',
        'description': 'description',
        'keywords': 'get_meta_keywords',
        'image_width': 600,
        'image_height': 600,
        'image': 'get_meta_image_url',
        'url': 'get_absolute_url',
        'use_facebook': True,
        'use_schemaorg': True,
        'use_twitter': True,
        'use_og': True,
    }

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL
        """

        return reverse('product', kwargs={'product_id': self.id})

    def get_meta_image_url(self) -> str:
        assert self.thumbnail.url is not None

        return self.thumbnail.url

    def get_meta_keywords(self) -> list[str]:
        """
        Returns the keywords
        """

        return [keyword.keyword for keyword in self.keywords.all()]

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class ProductKeyword(models.Model):
    """
    Model for product keywords
    """

    keyword = models.CharField(max_length=100)
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='keywords')

    def __str__(self):
        """
        Returns the keyword
        """

        return self.keyword


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


class Project(ModelMeta, models.Model):
    """
    Model for projects
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='project/thumbnails/',
                                  force_format='WEBP', quality=75)
    name = models.CharField(max_length=100)
    construction_date = models.DateField()
    products = models.ManyToManyField('Product', related_name='projects')
    colors = models.ManyToManyField('Color', related_name='colors')
    city = models.CharField(max_length=100)

    # The metadata.
    _metadata = {
        'title': 'name',
        'description': 'description',
        'keywords': 'get_meta_keywords',
        'image_width': 600,
        'image_height': 600,
        'image': 'get_meta_image_url',
        'url': 'get_absolute_url',
        'use_facebook': True,
        'use_schemaorg': True,
        'use_twitter': True,
        'use_og': True,
    }

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL
        """

        return reverse('project', kwargs={'project_id': self.id})

    def get_meta_image_url(self) -> str:
        assert self.thumbnail.url is not None

        return self.thumbnail.url

    def get_meta_keywords(self) -> list[str]:
        """
        Returns the keywords
        """

        return [keyword.keyword for keyword in self.keywords.all()]

    def __str__(self):
        """
        Returns the name
        """

        return self.name


class ProjectKeyword(models.Model):
    """
    Model for project keywords
    """

    keyword = models.CharField(max_length=100)
    project = models.ForeignKey('Project',
                                on_delete=models.CASCADE,
                                related_name='keywords')

    def __str__(self):
        """
        Returns the keyword
        """

        return self.keyword


class ProjectPicture(models.Model):
    """
    Model for project pictures
    """

    picture = ResizedImageField(size=[750, 500], crop=['middle', 'center'], upload_to='newest_projects/banners/',
                                force_format='WEBP', quality=75)
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


class Post(ModelMeta, models.Model):
    """
    Model for newest_projects
    """

    thumbnail = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='newest_projects/thumbnails/',
                                  force_format='WEBP', quality=75)
    banner = ResizedImageField(size=[1920, 720], crop=['middle', 'center'], upload_to='newest_projects/banners/',
                               force_format='WEBP', quality=75)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    date = models.DateField()

    # The metadata.
    _metadata = {
        'title': 'name',
        'description': 'description',
        'keywords': 'get_meta_keywords',
        'image_width': 600,
        'image_height': 600,
        'image': 'get_meta_image_url',
        'url': 'get_absolute_url',
        'use_facebook': True,
        'use_schemaorg': True,
        'use_twitter': True,
        'use_og': True,
    }

    def get_absolute_url(self) -> str:
        """
        Returns the absolute URL
        """

        return reverse('post', kwargs={'post_id': self.id})

    def get_meta_image_url(self) -> str:
        assert self.thumbnail.url is not None

        return self.thumbnail.url

    def get_meta_keywords(self) -> list[str]:
        """
        Returns the keywords
        """

        return [keyword.keyword for keyword in self.keywords.all()]

    def __str__(self):
        """
        Returns the title
        """

        return self.title


class PostKeyword(models.Model):
    """
    Model for post keywords
    """

    keyword = models.CharField(max_length=100)
    post = models.ForeignKey('Post',
                             on_delete=models.CASCADE,
                             related_name='keywords')

    def __str__(self):
        """
        Returns the keyword
        """

        return self.keyword


class QAndA(models.Model):
    """
    Model for Q&A
    """

    question = models.CharField(max_length=100)
    answer = RichTextUploadingField()

    class Meta:
        verbose_name = 'Q&A'
        verbose_name_plural = 'Q&As'

    def __str__(self):
        """
        Returns the question
        """

        return self.question


class ConsultationRequest(models.Model):
    """
    Model for consultation_form requests
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    notified = models.BooleanField()

    def __str__(self):
        """
        Returns the name.
        """

        return "Consultation request by " + self.name
