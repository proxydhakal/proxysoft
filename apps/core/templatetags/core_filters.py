from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def _youtube_video_id(url: str) -> str:
    try:
        from urllib.parse import urlparse, parse_qs
    except Exception:
        return ""
    if not url:
        return ""
    u = str(url).strip()
    if not u:
        return ""
    parsed = urlparse(u)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").strip("/")
    qs = parse_qs(parsed.query or "")

    # youtu.be/<id>
    if host.endswith("youtu.be"):
        return path.split("/")[0] if path else ""

    # youtube.com/watch?v=<id>
    if "v" in qs and qs["v"]:
        return qs["v"][0]

    # youtube.com/embed/<id>, youtube.com/shorts/<id>
    if "youtube" in host:
        parts = path.split("/")
        if len(parts) >= 2 and parts[0] in {"embed", "shorts"}:
            return parts[1]
    return ""


@register.filter
def youtube_embed(url):
    """Convert a YouTube URL to an embed URL (or empty string)."""
    vid = _youtube_video_id(url)
    if not vid:
        return ""
    return f"https://www.youtube.com/embed/{vid}"



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


@register.filter
def digits_only(value):
    """Keep only digits from a phone-like string (for wa.me links)."""
    if value is None:
        return ""
    s = str(value)
    return "".join(ch for ch in s if ch.isdigit())
