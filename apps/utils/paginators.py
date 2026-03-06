from django.core.paginator import Paginator
from django.conf import settings
from django.core.exceptions import ValidationError

def paginate_and_sort(request, objects, default_sort_field, allowed_fields, documents_per_page=settings.MAX_DOCUMENTS_PER_PAGE):
    page_number = request.GET.get('page', 1)
    sort_field = request.GET.get('sort_field', default_sort_field)
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_field not in allowed_fields:
        raise ValidationError("Champ non autorisé.")
    if sort_order== 'asc':
        objects = objects.order_by(sort_field)
    else: 
        objects = objects.order_by("-" + sort_field)
    paginator = Paginator(objects, documents_per_page)
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
        'sort_field': sort_field,
        'sort_order': sort_order
    }
