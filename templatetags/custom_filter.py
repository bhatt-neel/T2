from django import template
register = template.Library()

@register.filter(name="SampleTag")
def sampleTag(hello):
    return hello
