import copy
import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .filters import PhraseFilter
from .generator import clean_data, generate
from name_generator.settings import COUNT
from .models import History, User
from .serializers import PhraseSerializer


class PhraseViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = PhraseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PhraseFilter
    http_method_names = ['get', 'delete']

    def get_queryset(self):
        if not self.request.query_params.get('user_id', False):
            raise ValidationError('user_id is required')
        return History.objects.all()


class MapViewSet(views.APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        if not data:
            raise ValidationError('data is required')
        count = request.data.get('count')
        if count > COUNT:
            raise ValidationError(
                f'Количество генераций не может быть больше {COUNT}'
            )
        local_id = request.data.get('id')
        [*result] = (
            generate(clean_data(copy.deepcopy(data))) for _ in range(count)
        )
        if local_id is None:
            local_id = random.randint(0, 10**6)
        user, _ = User.objects.get_or_create(local_id=local_id)
        History.objects.bulk_create(
            [History(user=user, phrase=phrase) for phrase in result]
        )
        return Response(
            {'data': result, 'id': local_id},
            status=status.HTTP_201_CREATED
        )
