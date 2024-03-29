from django import forms


class ContactForm(forms.Form):
    """
    The map for the contact us page
    """

    name = forms.CharField(min_length=3, max_length=50, required=True)
    phone = forms.CharField(min_length=10, max_length=30, required=True)
    message = forms.CharField(min_length=10, max_length=10000, required=True)


class ConsultRequestForm(forms.Form):
    """
    The map for the consultation_form request
    """

    name = forms.CharField(min_length=3, max_length=50, required=True)
    phone = forms.CharField(min_length=10, max_length=30, required=True)
