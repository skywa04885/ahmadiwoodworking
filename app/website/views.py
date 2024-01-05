from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import QAndA, Post, ContactMessage, Project, Product, ProjectPicture, Color, ProductAdvantage, \
    ProductDisadvantage
from .forms import ContactForm


def index(request: HttpRequest) -> HttpResponse:
    """
    This view handles the index page.
    """

    newest_products: QuerySet[Product] = Product.objects.all().order_by('-id')[:6]
    highest_rated_products: QuerySet[Product] = Product.objects.all()[:3]

    # Get the Q&A and posts.
    q_and_as: QuerySet[QAndA] = QAndA.objects.all()
    posts: QuerySet[Post] = Post.objects.all().order_by('-date')[:4]

    # Render the index page.
    return render(request, 'index.html', {
        'q_and_as': q_and_as,
        'posts': posts,
        'newest_products': newest_products,
        'highest_rated_products': highest_rated_products
    })


def contact(request: HttpRequest) -> HttpResponse:
    """
    This view handles the contact form.
    """

    # Check if the form has been submitted.
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request.
        form = ContactForm(request.POST)

        # Get the form data.
        name, phone, message = form.data['name'], form.data['phone'], form.data['message']

        # Check if the form is valid.
        if form.is_valid():
            # Send email to the website owner.
            no_sent_messages = send_mail(f'Contact notification for submission by {name}',
                                         f'Name: {name}\nPhone: {phone}\nMessage: {message}',
                                         settings.CONTACT_NOTIFICATION_FROM_ADDRESS,
                                         settings.CONTACT_NOTIFICATION_TO_ADDRESSES,
                                         fail_silently=True)

            # Save the contact message to the database.
            contact_message = ContactMessage(name=name, phone=phone, message=message, notified=no_sent_messages == len(
                settings.CONTACT_NOTIFICATION_TO_ADDRESSES))
            contact_message.save()

            return redirect('contact-thanks')
    else:
        form = ContactForm()

    # Render the contact page.
    return render(request, 'contact.html', {'form': form})


def post(request: HttpRequest, post_id) -> HttpResponse:
    """
    This view handles the post page.
    """

    # Get the post.
    post = Post.objects.get(pk=post_id)

    # Render the post page.
    return render(request, 'post.html', {'post': post})


def about(request: HttpRequest) -> HttpResponse:
    """
    This view handles the about page.
    """

    return render(request, 'about.html')


def contact_thanks(request: HttpRequest) -> HttpResponse:
    """
    This view handles the contact form.
    """

    return render(request, 'contact-thanks.html')


def portfolio(request: HttpRequest) -> HttpResponse:
    """
    This view handles the portfolio page.
    """

    # Get the query and page number from the request.
    query: str | None = request.GET.get('query')
    page: int = request.GET.get('page', 1)

    # Get the projects.
    query_set: QuerySet[Project] = Project.objects.filter(name__icontains=query) if query else Project.objects.all()
    paginator: Paginator = Paginator(query_set, 3)
    page: Page = paginator.get_page(page)

    # Render the portfolio page.
    return render(request, 'portfolio.html', {
        'page': page,
    })


# noinspection PyShadowingNames
def project(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    This view handles the project page.
    """

    # Get the project.
    project: Project = Project.objects.get(pk=project_id)

    # Gets all the products, pictures and colors,
    products: QuerySet[Product] = project.products.all()
    pictures: QuerySet[ProjectPicture] = project.pictures.all()
    colors: QuerySet[Color] = project.colors.all()

    # Constructs a list containing all the picture urls from the pictures list.
    picture_urls: list[str] = [picture.picture.url for picture in pictures]

    # Render the project page.
    return render(request, 'project.html', {
        'project': project,
        'products': products,
        'pictures': pictures,
        'colors': colors,
        'picture_urls': picture_urls
    })


# noinspection PyShadowingNames
def product(request: HttpRequest, product_id: int) -> HttpResponse:
    # Get the product and it's advantages and disadvantages.
    product: Product = Product.objects.get(pk=product_id)
    advantages: QuerySet[ProductAdvantage] = product.advantages.all()
    disadvantages: QuerySet[ProductDisadvantage] = product.disadvantages.all()

    # Gets the latest 4 posts.
    posts: QuerySet[Post] = Post.objects.all().order_by('-date')[:4]

    # Gets all the projcets using this product.
    projects: QuerySet[Project] = product.projects.all()

    # Renders the product page.
    return render(request, 'product.html', {
        'product': product,
        'advantages': advantages,
        'disadvantages': disadvantages,
        'posts': posts,
        'projects': projects
    })

# noinspection PyShadowingNames
def post(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    This view handles the post page.
    """

    post = Post.objects.get(pk=post_id)

    return render(request, 'post.html', {
        'post': post
    })
