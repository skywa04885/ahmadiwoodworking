from typing import Dict, Any, List

from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from meta.views import Meta

from .models import (
    QAndA,
    Post,
    ContactMessage,
    Project,
    Product,
    ProjectPicture,
    Color,
    ProductAdvantage,
    ProductDisadvantage,
    ConsultationRequest,
)
from .forms import ContactForm, ConsultRequestForm


# noinspection PyShadowingNames
def footer_context() -> Dict[str, Any]:
    """
    This function returns the context for the footer.
    """

    # Gets the footer context.
    products: QuerySet[Product] = Product.objects.all()[:10]
    posts: QuerySet[Post] = Post.objects.all()[:10]

    # Returns the footer context.
    return {
        "products": products,
        "posts": posts,
    }


def index(request: HttpRequest) -> HttpResponse:
    """
    This view handles the index page.
    """

    newest_products: QuerySet[Product] = Product.objects.all().order_by("-id")[:6]
    highest_rated_products: QuerySet[Product] = Product.objects.all()[:3]
    q_and_as: QuerySet[QAndA] = QAndA.objects.all()
    newest_posts: QuerySet[Post] = Post.objects.all().order_by("-date")[:4]
    newest_projects: QuerySet[Project] = Project.objects.all().order_by("-id")[:4]

    # Render the index page.
    return render(
        request,
        "index.html",
        {
            "q_and_as": q_and_as,
            "newest_posts": newest_posts,
            "newest_products": newest_products,
            "highest_rated_products": highest_rated_products,
            "newest_projects": newest_projects,
        },
    )


def contact(request: HttpRequest) -> HttpResponse:
    """
    This view handles the contact map.
    """

    # Check if the map has been submitted.
    if request.method == "POST":
        # Create a map instance and populate it with data from the request.
        form = ContactForm(request.POST)

        # Check if the map is valid.
        if form.is_valid():
            # Get the map data.
            name, phone, message = (
                form.data["name"],
                form.data["phone"],
                form.data["message"],
            )

            # Get the email templates.
            txt_template = get_template("website/mail/contact_notification.txt")
            html_template = get_template("website/mail/contact_notification.html")

            # Render the email templates.
            txt_content = txt_template.render(
                {"name": name, "phone": phone, "message": message}
            )
            html_content = html_template.render(
                {"name": name, "phone": phone, "message": message}
            )

            # Send email to the website owner.
            n_messages_sent = send_mail(
                subject="Contact notification",
                message=txt_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=settings.CONTACT_NOTIFICATION_TO_ADDRESSES,
                fail_silently=False,
                html_message=html_content,
            )
            notified = n_messages_sent == len(
                settings.CONTACT_NOTIFICATION_TO_ADDRESSES
            )

            # Save the contact message to the database.
            contact_message = ContactMessage(
                name=name, phone=phone, message=message, notified=notified
            )
            contact_message.save()

            return render(request, "website/pages/contact.html", {
                "contact_message": contact_message,
            })
    else:
        form = ContactForm()

    # Render the contact page.
    return render(request, "website/pages/contact.html", {"form": form})


def about(request: HttpRequest) -> HttpResponse:
    """
    This view handles the about page.
    """

    n_products: int = Product.objects.count()
    n_projects: int = Project.objects.count()

    return render(request, "website/pages/about.html", {
        "n_products": n_products,
        "n_projects": n_projects,
    })


def portfolio(request: HttpRequest) -> HttpResponse:
    """
    This view handles the portfolio page.
    """

    # Get the query and page number from the request.
    query: str | None = request.GET.get("query")
    page: int = request.GET.get("page", 1)

    # Get the projects.
    query_set: QuerySet[Project] = (
        Project.objects.filter(name__icontains=query)
        if query
        else Project.objects.all()
    )
    paginator: Paginator = Paginator(query_set, 3)
    page: Page = paginator.get_page(page)

    # Render the portfolio page.
    return render(
        request,
        "website/pages/portfolio.html",
        {
            "page": page,
            "query": query,
        },
    )


# noinspection PyShadowingNames
def project(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    This view handles the project page.
    """

    # Get the project.
    project: Project = Project.objects.get(pk=project_id)

    # Gets the project meta.
    meta: Meta = project.as_meta(request)

    # Gets all the products, pictures and colors,
    products: QuerySet[Product] = project.products.all()
    pictures: QuerySet[ProjectPicture] = project.pictures.all()
    colors: QuerySet[Color] = project.colors.all()

    # Constructs a list containing all the picture urls from the pictures list.
    picture_urls: list[str] = [picture.picture.url for picture in pictures]

    consult_request_form = ConsultRequestForm()

    # Render the project page.
    return render(
        request,
        "website/pages/project.html",
        {
            "project": project,
            "products": products,
            "pictures": pictures,
            "colors": colors,
            "picture_urls": picture_urls,
            "consult_request_form": consult_request_form,
            "meta": meta,
        },
    )


# noinspection PyShadowingNames
def product(request: HttpRequest, product_id: int) -> HttpResponse:
    # Get the product and it's advantages and disadvantages.
    product: Product = Product.objects.get(pk=product_id)
    advantages: QuerySet[ProductAdvantage] = product.advantages.all()
    disadvantages: QuerySet[ProductDisadvantage] = product.disadvantages.all()

    # Gets the product meta.
    meta: Meta = product.as_meta(request)

    # Gets the latest 4 newest_projects.
    posts: QuerySet[Post] = Post.objects.all().order_by("-date")[:4]

    # Gets all the projects using this product.
    projects: QuerySet[Project] = product.projects.all()

    # Gets the consultation_form request map.
    consult_request_form = ConsultRequestForm()

    # Renders the product page.
    return render(
        request,
        "website/pages/product.html",
        {
            "product": product,
            "advantages": advantages,
            "disadvantages": disadvantages,
            "posts": posts,
            "projects": projects,
            "consult_request_form": consult_request_form,
            "meta": meta
        },
    )


def request_consultation(request: HttpRequest) -> HttpResponse:
    """
    This view handles the consultation_form request map.
    """

    # Check if the map has been submitted.
    if request.method == "POST":
        # Get the redirection target from the request.
        redirection_target: str = request.POST.get("redirection_target", "index")

        # Create a map instance and populate it with data from the request.
        form = ConsultRequestForm(request.POST)

        # Get the map data.
        name, phone = form.data["name"], form.data["phone"]

        # Check if the map is valid.
        if form.is_valid():
            # Get the email templates.
            txt_template = get_template("website/mail/consultation_notification.txt")
            html_template = get_template("website/mail/consultation_notification.html")

            # Render the email templates.
            txt_content = txt_template.render({"name": name, "phone": phone})
            html_content = html_template.render({"name": name, "phone": phone})

            # Send email to the website owner.
            n_messages_sent = send_mail(
                subject="Consultation request notification",
                message=txt_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=settings.CONSULTATION_REQUEST_NOTIFICATION_TO_ADDRESSES,
                fail_silently=True,
                html_message=html_content,
            )
            notified = n_messages_sent == len(
                settings.CONSULTATION_REQUEST_NOTIFICATION_TO_ADDRESSES
            )

            # Save the consultation_form request to the database.
            consultation_request = ConsultationRequest(
                name=name, phone=phone, notified=notified
            )
            consultation_request.save()

            # Redirect to the redirection target.
            return redirect(redirection_target)
    else:
        return HttpResponseBadRequest("Invalid request.")


def products(request: HttpRequest) -> HttpResponse:
    """
    View function for displaying all products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered products page.
    """

    # Get the query and page number from the request.
    query: str | None = request.GET.get("query")
    page: int = request.GET.get("page", 1)

    # Get the products.
    query_set: QuerySet[Product] = (
        Product.objects.filter(name__icontains=query)
        if query
        else Product.objects.all()
    )

    # Performs the pagination.
    paginator: Paginator = Paginator(query_set, 3)
    page: Page = paginator.get_page(page)

    # Renders the products page.
    return render(request, "website/pages/products.html", {"page": page, "query": query})


def posts(request: HttpRequest) -> HttpResponse:
    """
    View function for displaying all newest_projects.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered newest_projects page.
    """

    # Get the query and page number from the request.
    query: str | None = request.GET.get("query")
    page: int = request.GET.get("page", 1)

    # Get the newest_projects.
    query_set: QuerySet[Product] = (
        Post.objects.filter(title__icontains=query)
        if query
        else Post.objects.all()
    )

    # Performs the pagination.
    paginator: Paginator = Paginator(query_set, 12)
    page: Page = paginator.get_page(page)

    # Renders the products page.
    return render(request, "website/pages/posts.html", {
        "page": page,
        "query": query
    })


# noinspection PyShadowingNames
def post(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    View function for displaying a post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post to display.

    Returns:
        HttpResponse: The HTTP response object containing the rendered post page.
    """

    # Get the post.
    post: Post = Post.objects.get(pk=post_id)

    # Gets the post meta.
    meta: Meta = post.as_meta(request)

    # Gets some other newest_projects.
    other_posts: QuerySet[Post] = Post.objects.exclude(pk=post.pk).order_by("-date")[:4]

    # Renders the post page.
    return render(request, "website/pages/post.html", {
        "post": post,
        "other_posts": other_posts,
        "meta": meta,
    })
