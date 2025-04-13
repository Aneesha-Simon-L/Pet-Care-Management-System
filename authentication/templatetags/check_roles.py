from django import template

register = template.Library()

@register.simple_tag
def check_user_roles(request,roles):

    roles = roles.split(',')

    allow = False

    if request.user.role in roles:

        allow = True
    
    return allow
