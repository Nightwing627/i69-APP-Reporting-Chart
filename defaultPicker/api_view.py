from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response

from defaultPicker import models, serializers


class DefaultPickersView(APIView):
    def get(self, request):
        pickers = {}

        def get_all(key, serializer, model):
            pickers[key] = serializer(model.objects.all(), many=True).data

        get_all("ages", serializers.AgeSerializer, models.age)
        get_all("ethnicity", serializers.EthnicitySerializer, models.ethnicity)
        get_all("family", serializers.FamilySerializer, models.family)
        get_all("genders", serializers.GenderSerilizer, models.gender)
        get_all("heights", serializers.HeightSerilizer, models.height)
        get_all("politics", serializers.PoliticsSerializer, models.politics)
        get_all("religious", serializers.ReligiousSerializer, models.religious)
        get_all("searchGenders", serializers.SearchGenderSerializer, models.searchGender)
        get_all("tags", serializers.TagsSerializer, models.tags),
        get_all("zodiacSigns", serializers.ZodiacSignSerializer, models.zodiacSign)

        return Response({"defaultPickers": pickers})


default_picker_view = DefaultPickersView.as_view()
