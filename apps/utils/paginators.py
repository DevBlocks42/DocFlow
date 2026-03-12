from django.core.paginator import Paginator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import DateField, DateTimeField, CharField, ForeignKey
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
        print(field, type(field))
        if isinstance(field, (DateField, DateTimeField)):
            try:
                filter = datetime.strptime(filter, "%d/%m/%y").date()
            except ValueError:
                try:
                    filter = datetime.strptime(filter, "%d/%m").date()
                    filter = filter.replace(year=datetime.now().year)
                except Exception:
                    raise ValidationError("Format de date invalide, veuillez saisir une date au format jj/mm/yy ou jj/mm") 
        elif field.choices:
            print("CONDITION") 
            raw_value = get_choice_value_from_display(field.choices, filter)
            if raw_value:
                objects = objects.filter(**{filter_field: raw_value})
            else:
                objects = objects.none()
        elif isinstance(field, ForeignKey):
            target_field = field.remote_field.model._meta.get_field(filter_field.split("__")[1])
            if isinstance(target_field, CharField) and target_field.choices:
                raw_value = get_choice_value_from_display(target_field.choices, filter)
                if raw_value:
                    objects = objects.filter(**{filter_field: raw_value})
            else:
                objects = objects.filter(**{f"{filter_field}__icontains": filter})
        else:
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

def get_choice_value_from_display(choices, display_value):
    display_value = display_value.lower()
    for value, label in choices:
        ##Comparaison partielle => utiliser un select sur le choix possibles
        if label.lower() == display_value:
            return value
    return None