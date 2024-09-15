import random
import string
import re
from unidecode import unidecode


def generate_url_slug(title, length=6, max_slug_length=50):
    title = unidecode(title)
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    if slug and slug[0].isdigit():
        slug = 'n-' + slug
    if len(slug) > max_slug_length:
        slug = slug[:max_slug_length].rsplit('-', 1)[0]
    random_string = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=length))
    unique_slug = f"{slug}-{random_string}"

    return unique_slug
