from django.core.paginator import Paginator, Page
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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


def index(request: HttpRequest) -> HttpResponse:
    """
    This view handles the index page.
    """

    newest_products: QuerySet[Product] = Product.objects.all().order_by("-id")[:6]
    highest_rated_products: QuerySet[Product] = Product.objects.all()[:3]

    # Get the Q&A and posts.
    q_and_as: QuerySet[QAndA] = QAndA.objects.all()
    posts: QuerySet[Post] = Post.objects.all().order_by("-date")[:4]

    # Render the index page.
    return render(
        request,
        "index.html",
        {
            "q_and_as": q_and_as,
            "posts": posts,
            "newest_products": newest_products,
            "highest_rated_products": highest_rated_products,
        },
    )


def contact(request: HttpRequest) -> HttpResponse:
    """
    This view handles the contact form.
    """

    # Check if the form has been submitted.
    if request.method == "POST":
        # Create a form instance and populate it with data from the request.
        form = ContactForm(request.POST)

        # Get the form data.
        name, phone, message = (
            form.data["name"],
            form.data["phone"],
            form.data["message"],
        )

        # Check if the form is valid.
        if form.is_valid():
            # Get the email templates.
            txt_template = get_template("website/mail/contact_notification.txt")
            html_template = get_template("website/mail/contact_notification.html")

            # Render the email templates.
            txt_content = txt_template.render({"name": name, "phone": phone, "message": message})
            html_content = html_template.render({"name": name, "phone": phone, "message": message})

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
                name=name,
                phone=phone,
                message=message,
                notified=notified
            )
            contact_message.save()

            return redirect("contact-thanks")
    else:
        form = ContactForm()

    # Render the contact page.
    return render(request, "contact.html", {"form": form})


def post(request: HttpRequest, post_id) -> HttpResponse:
    """
    This view handles the post page.
    """

    # Get the post.
    post = Post.objects.get(pk=post_id)

    # Render the post page.
    return render(request, "post.html", {"post": post})


def about(request: HttpRequest) -> HttpResponse:
    """
    This view handles the about page.
    """

    return render(request, "about.html")


def contact_thanks(request: HttpRequest) -> HttpResponse:
    """
    This view handles the contact form.
    """

    return render(request, "contact-thanks.html")


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
        "portfolio.html",
        {
            "page": page,
        },
    )


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

    consult_request_form = ConsultRequestForm()

    # Render the project page.
    return render(
        request,
        "project.html",
        {
            "project": project,
            "products": products,
            "pictures": pictures,
            "colors": colors,
            "picture_urls": picture_urls,
            "consult_request_form": consult_request_form,
        },
    )


# noinspection PyShadowingNames
def product(request: HttpRequest, product_id: int) -> HttpResponse:
    # Get the product and it's advantages and disadvantages.
    product: Product = Product.objects.get(pk=product_id)
    advantages: QuerySet[ProductAdvantage] = product.advantages.all()
    disadvantages: QuerySet[ProductDisadvantage] = product.disadvantages.all()

    # Gets the latest 4 posts.
    posts: QuerySet[Post] = Post.objects.all().order_by("-date")[:4]

    # Gets all the projects using this product.
    projects: QuerySet[Project] = product.projects.all()

    consult_request_form = ConsultRequestForm()

    # Renders the product page.
    return render(
        request,
        "product.html",
        {
            "product": product,
            "advantages": advantages,
            "disadvantages": disadvantages,
            "posts": posts,
            "projects": projects,
            "consult_request_form": consult_request_form,
        },
    )


def request_consultation(request: HttpRequest) -> HttpResponse:
    """
    This view handles the consultation request form.
    """

    # Check if the form has been submitted.
    if request.method == "POST":
        # Get the redirection target from the request.
        redirection_target: str = request.GET.get("redirection_target", "index")

        # Create a form instance and populate it with data from the request.
        form = ConsultRequestForm(request.POST)

        # Get the form data.
        name, phone = form.data["name"], form.data["phone"]

        # Check if the form is valid.
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

            # Save the consultation request to the database.
            consultation_request = ConsultationRequest(
                name=name, phone=phone, company_notified=notified
            )
            consultation_request.save()

            # Redirect to the redirection target.
            return redirect(redirection_target)
    else:
        return HttpResponseBadRequest("Invalid request.")
