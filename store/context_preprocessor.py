from django.db.models import Prefetch
from store.models import Category, Service


def include_categories_to_nav_bar(request):
    queryset = Category.objects.prefetch_related(
        Prefetch(
            'service_set',
            Service.objects.all(),
            to_attr='services'
        )
    )

    return {'categories': queryset}


