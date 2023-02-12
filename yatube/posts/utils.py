from django.core.paginator import Paginator

POSTS_PER_PAGE = 10


def get_pag(obj, request):
    paginator = Paginator(obj, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj
    }
