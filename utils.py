from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

SORT_NAME = settings.get('GENERIC_EDIT_SORT_NAME', 'sort')
PAGE_NAME = settings.get('GENERIC_EDIT_PAGE_NAME', 'page')

def sort_q(request, queryset, sort_fields, default_sort):
    valid_sorts = (('%s' % field, '-%s' % field) for field in sort_fields)
    valid_sorts = (item for sublist in valid_sorts for item in sublist)

    sort_in_get = SORT_NAME in request.GET and request.GET[SORT_NAME] in valid_sorts
    sort_mode = request.GET[SORT_NAME] if sort_in_get else default_sort

    return queryset.order_by(sort_mode), sort_mode


def paginate_q(request, queryset, results_per_page=20):
    paginator = Paginator(queryset, results_per_page)

    try:
        pagenum = int(request.GET.get(PAGE_NAME, '1'))
    except ValueError:
        pagenum = 1

    try:
        resultset = paginator.page(pagenum)
    except (EmptyPage, InvalidPage):
        resultset = paginator.page(paginator.num_pages)

    return paginator, pagenum, resultset

