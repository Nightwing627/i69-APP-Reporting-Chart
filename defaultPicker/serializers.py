from django.db.models.base import ModelState
from rest_framework import fields, serializers
from defaultPicker import models

class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.age
        fields = '__all__'

class HeightSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.height
        fields = '__all__'

class GenderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.gender
        fields = '__all__'

class SearchGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.searchGender
        fields = '__all__'

class EthnicitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ethnicity
        fields = '__all__'

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.family
        fields = '__all__'

class PoliticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.politics
        fields = '__all__'

class ReligiousSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.religious
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tags
        fields = '__all__'

class ZodiacSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.zodiacSign
        fields = '__all__'

class InterestedInSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.interestedIn
        fields = '__all__'

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.config
        fields = '__all__'

class TvShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tvShows
        fields = '__all__'

class SportsTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.sportsTeams
        fields = '__all__'

class MoviesSerialzier(serializers.ModelSerializer):
    class Meta:
        model = models.movies
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.book
        fields = '__all__'