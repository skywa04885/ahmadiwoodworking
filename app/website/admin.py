from django.contrib import admin
from .models import Post, QAndA, Product, ProductAdvantage, ProductDisadvantage, Project, ContactMessage, \
    ProjectPicture, Color


@admin.register(ProductAdvantage)
class ProductAdvantageAdmin(admin.ModelAdmin):
    """
    This class handles the product advantage admin page.
    """

    pass


class ProductAdvantageInline(admin.TabularInline):
    """
    This class handles the product advantage inline.
    """

    model = ProductAdvantage
    extra = 1


@admin.register(ProductDisadvantage)
class ProductDisadvantageAdmin(admin.ModelAdmin):
    """
    This class handles the product disadvantage admin page.
    """

    pass


class ProductDisadvantageInline(admin.TabularInline):
    """
    This class handles the product disadvantage inline.
    """

    model = ProductDisadvantage
    extra = 1


class ProjectPictureInline(admin.TabularInline):
    """
    This class handles the project picture inline.
    """

    model = ProjectPicture
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    This class handles the product admin page.
    """

    inlines = [ProductAdvantageInline, ProductDisadvantageInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    This class handles the project admin page.
    """

    filter_horizontal = ('products',)
    inlines = [ProjectPictureInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    This class handles the contact message admin page.
    """

    readonly_fields = ('notified', 'name', 'phone', 'message')

    def has_add_permission(self, request, obj=None):
        """
        This method handles the add permission.
        """

        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    This class handles the post admin page.
    """

    pass


@admin.register(QAndA)
class QAndAAdmin(admin.ModelAdmin):
    """
    This class handles the Q&A admin page.
    """

    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    """
    This class handles the color admin page.
    """

    pass
