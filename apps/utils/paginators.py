from django.core.paginator import Paginator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import DateField, DateTimeField
from datetime import datetime

def paginate_sort_and_filter(page_number, sort_field, sort_order, filter_field, filter, objects, default_sort_field, allowed_fields, documents_per_page=settings.MAX_DOCUMENTS_PER_PAGE):
    if sort_field not in allowed_fields or (filter_field and filter_field not in allowed_fields):
        raise ValidationError("Champ non autorisé.")
    if sort_order== 'asc':
        objects = objects.order_by(sort_field)
    else: 
        objects = objects.order_by("-" + sort_field)
    if filter_field and filter:
        model = objects.model
        field = model._meta.get_field(filter_field.split("__")[0])
        if isinstance(field, (DateField, DateTimeField)):
            try:
                filter = datetime.strptime(filter, "%d/%m/%y").date()
            except ValueError:
                try:
                    filter = datetime.strptime(filter, "%d/%m").date()
                    filter = filter.replace(year=datetime.now().year)
                except Exception:
                    raise ValidationError("Format de date invalide, veuillez saisir une date au format jj/mm/yy ou jj/mm") 
        objects = objects.filter(**{f"{filter_field}__icontains": filter})
    paginator = Paginator(objects, documents_per_page)
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'filter_field': filter_field,
        'filter': filter
    }
