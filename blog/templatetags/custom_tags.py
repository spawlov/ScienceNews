from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    parameters = context["request"].GET.copy()
    for key, value in kwargs.items():
        parameters[key] = value
    return parameters.urlencode()
