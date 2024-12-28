from django_filters.rest_framework import filters, FilterSet

from .models import History, User


class PhraseFilter(FilterSet):
    user_id = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='user_id',
        to_field_name='local_id',
    )

    class Meta:
        model = History
        fields = ('user_id',)
