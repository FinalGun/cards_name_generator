from rest_framework import serializers

from .models import History


class PhraseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ['id', 'phrase', 'user']

    def get_user(self, obj):
        return obj.user.local_id
