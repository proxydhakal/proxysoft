from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(value, word):
    """Wrap the first occurrence of `word` in value with <span class='text-proxyCyan'>."""
    if not value or not word:
        return value
    word = str(word)
    if word not in value:
        return value
    before, _, after = value.partition(word)
    return mark_safe(f"{before}<span class='text-proxyCyan'>{word}</span>{after}")


@register.filter
def csv_list(value):
    """Split a comma-separated string into a list of trimmed items."""
    if not value:
        return []
    return [s.strip() for s in str(value).split(",") if s and s.strip()]
