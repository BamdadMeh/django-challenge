from rest_framework.serializers import ModelSerializer

from apps.stadium.models import Stadium


class StadiumSerializer(ModelSerializer):

    class Meta:
        model = Stadium
        fields = ('name', 'slug')

        extra_kwargs = {

            'slug': {
                'read_only': True,
            },

        }
