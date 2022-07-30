from django.db import models
import graphene
from graphene import *
from .models import age, ethnicity, politics, religious, family, zodiacSign, tags, interestedIn, gender, height, \
    searchGender, config
from django.db.models import F


class ageObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Int()
    value_fr = graphene.Int()


class heightObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.Int()
    value_fr = graphene.Int()


class ethnicityObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class familyObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class genderObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class searchGenderObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class politicsObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class religiousObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class tagsObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class zodiacSignObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class interestedInObj(graphene.ObjectType):
    id = graphene.Int()
    value = graphene.String()
    value_fr = graphene.String()


class configObj(graphene.ObjectType):
    id = graphene.Int()
    message = graphene.String()
    imageMessage = graphene.String()
    avatarPhoto = graphene.Int()


class AllPickers(graphene.ObjectType):
    agePicker = graphene.List(ageObj)
    ethnicityPicker = graphene.List(ethnicityObj)
    familyPicker = graphene.List(familyObj)
    genderPicker = graphene.List(genderObj)
    heightsPicker = graphene.List(heightObj)
    searchGendersPicker = graphene.List(searchGenderObj)
    politicsPicker = graphene.List(politicsObj)
    religiousPicker = graphene.List(religiousObj)
    tagsPicker = graphene.List(tagsObj)
    zodiacSignPicker = graphene.List(zodiacSignObj)
    configPicker = graphene.List(configObj)

    # interestedInPicker = graphene.List(interestedInObj)

    def resolve_agePicker(self, info):
        return age.objects.values('id', value=F('age'), value_fr=F('age'))

    def resolve_heightsPicker(self, info):
        return height.objects.values('id', value=F('height'), value_fr=F('height'))

    def resolve_genderPicker(self, info):
        return gender.objects.values('id', value=F('gender'), value_fr=F('gender_fr'))

    def resolve_searchGendersPicker(self, info):
        return searchGender.objects.values('id', value=F('searchGender'), value_fr=F('searchGender_fr'))

    def resolve_ethnicityPicker(self, info):
        return ethnicity.objects.values('id', value=F('ethnicity'), value_fr=F('ethnicity_fr'))

    def resolve_familyPicker(self, info):
        return family.objects.values('id', value=F('familyPlans'), value_fr=F('familyPlans_fr'))

    def resolve_politicsPicker(self, info):
        return politics.objects.values('id', value=F('politics'), value_fr=F('politics_fr'))

    def resolve_configPicker(self, info):
        return config.objects.values('id', message=F('coinsPerMessage'), imageMessage=F('coinsPerPhotoMessage'), avatarPhoto=F('coinsPerAvatarPhoto'))

    def resolve_religiousPicker(self, info):
        return religious.objects.values('id', value=F('religious'), value_fr=F('religious_fr'))

    def resolve_tagsPicker(self, info):
        return tags.objects.values('id', value=F('tag'), value_fr=F('tag_fr'))

    def resolve_zodiacSignPicker(self, info):
        return zodiacSign.objects.values('id', value=F('zodiacSign'), value_fr=F('zodiacSign_fr'))

    def resolve_interestedInPicker(self, info):
        return interestedIn.objects.values('id', value=F('interest'), value_fr=F('interest_fr'))


class Query(graphene.ObjectType):
    defaultPicker = graphene.Field(AllPickers)

    def resolve_defaultPicker(self, info):
        return AllPickers()
