from django.http import JsonResponse
from . import urlwrapper


def index(request, encoded_url, depth):
    root = urlwrapper.Uri(encoded_url)
    get_links_by_depth(root, depth)
    return JsonResponse(root.images, safe=False)


def get_link_url(link):
    return link.url


def get_links_by_depth(root, depth):
    if depth == 0:
        return
    data = root.get_all_relative_links()
    for l in data.links:
        get_links_by_depth(l, depth - 1)
