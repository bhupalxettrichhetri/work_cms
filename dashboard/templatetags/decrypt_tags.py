from django import template
from dashboard.encrypt_utils import decrypt

register = template.Library()


@register.filter
def decrypt_template_tag(value):
    print(value)
    return decrypt(value)


@register.filter
def document(value):
    print('there')
    return("here")