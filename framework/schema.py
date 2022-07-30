import graphene
import geopy.distance
from django.contrib.auth import get_user_model
from graphene.utils.resolve_only_args import resolve_only_args
import user.schema
import purchase.schema
import graphql_jwt
import graphene
from user.models import User, UserSocialProfile
from defaultPicker.models import tags, interestedIn, music as Music, movies as Movies, sportsTeams as SportsTeams, \
    tvShows as TVShow, book as Book, height as Height, age as Age
import reports.schema
# import purchase.schema
import defaultPicker.schema
from django.db.models import Q
import chatapp.schema
from gallery.models import Photo
from gallery.schema import PhotoObj
from django.db.models import Count
from user.schema import UserPhotoType
from graphql.error import GraphQLError

class TagResponse(graphene.ObjectType):
    id = graphene.Int()
    tag = graphene.String()
    tag_fr = graphene.String()


class AvatarPhotoMixin:
    avatar_photos = graphene.List(UserPhotoType)

    def resolve_avatar_photos(self, info):
        return self.avatar_photos.all()

class likedUsersResponse(graphene.ObjectType, AvatarPhotoMixin):
    id = graphene.String()
    username = graphene.String()
    full_name = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)


    def resolve_full_name(self, info):
        return self.fullName

    def resolve_id(self, info):
        return self.id

    def resolve_username(self, info):
        return self.username

    # depricated
    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))


class blockedUsersResponse(graphene.ObjectType, AvatarPhotoMixin):
    id = graphene.String()
    username = graphene.String()
    full_name = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)


    def resolve_full_name(self, info):
        return self.fullName

    def resolve_id(self, info):
        return self.id

    def resolve_username(self, info):
        return self.username

    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))


class InResponse(graphene.ObjectType):
    id = graphene.Int()
    interest = graphene.String()
    interest_fr = graphene.String()


class UserType(graphene.ObjectType, AvatarPhotoMixin):
    id = graphene.String()
    username = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    gender = graphene.Int()
    about = graphene.String()
    location = graphene.List(graphene.Float)
    isOnline = graphene.Boolean()
    familyPlans = graphene.Int()
    age = graphene.Int()
    tags = graphene.List(graphene.Int)
    politics = graphene.Int()
    coins = graphene.Int()
    zodiacSign = graphene.Int()
    height = graphene.Int()
    photos_quota = graphene.Int()
    interested_in = graphene.List(graphene.Int)
    ethinicity = graphene.Int()
    religion = graphene.Int()
    blocked_users = graphene.List(blockedUsersResponse)
    education = graphene.String()
    music = graphene.List(graphene.String)
    tvShows = graphene.List(graphene.String)
    sportsTeams = graphene.List(graphene.String)
    movies = graphene.List(graphene.String)
    work = graphene.String()
    books = graphene.List(graphene.String)
    avatar = graphene.String()
    avatar_photos = graphene.List(UserPhotoType)
    likes = graphene.List(likedUsersResponse)
    # depricated
    # photos = graphene.List(PhotoObj)

    def resolve_avatar_photos(self, info):
        return self.avatar_photos.all()

    @resolve_only_args
    def resolve_likes(self):
        user = get_user_model().objects.get(id=self.id)
        return user.likes.all()

    @resolve_only_args
    def resolve_age(self):
        user = get_user_model().objects.get(id=self.id)
        if user.age:
            return user.age.id
        return Age.objects.last().id

    @resolve_only_args
    def resolve_height(self):
        user = get_user_model().objects.get(id=self.id)
        if user.height:
            return user.height.id
        return Height.objects.last().id

    @resolve_only_args
    def resolve_likes(self):
        user = get_user_model().objects.get(id=self.id)
        return user.likes.all()

    @resolve_only_args
    def resolve_tvShows(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.tvShows.values_list('interest', flat=True))

    @resolve_only_args
    def resolve_location(self):
        user = get_user_model().objects.get(id=self.id)
        if user.location:
            return list(map(float, user.location.split(',')))
        return []

    @resolve_only_args
    def resolve_books(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.book.values_list('interest', flat=True))

    @resolve_only_args
    def resolve_sportsTeams(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.sportsTeams.values_list('interest', flat=True))

    @resolve_only_args
    def resolve_movies(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.movies.values_list('interest', flat=True))

    @resolve_only_args
    def resolve_music(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.music.values_list('interest', flat=True))
    
    # depricated
    # @resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))

    @resolve_only_args
    def resolve_tags(self):
        user = get_user_model().objects.get(id=self.id)
        return list(user.tags.values_list('id', flat=True))

    @resolve_only_args
    def resolve_interested_in(self):
        user = get_user_model().objects.get(id=self.id)
        return user.interestedIn_display

    @resolve_only_args
    def resolve_blocked_users(self):
        user = get_user_model().objects.get(id=self.id)
        return user.blockedUsers.all()


class userResponseObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    # depricated
    # photos = graphene.List(PhotoObj)
    interested_in = graphene.List(graphene.Int)

    # depricated
    # @graphene.resolve_only_args
    # def resolve_photos(self):
    #     return Photo.objects.values('id', 'image_data', 'date').filter(user=get_user_model().objects.get(id=self.id))

    @graphene.resolve_only_args
    def resolve_interested_in(self):
        return get_user_model().objects.get(id=self.id).interestedIn_display


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        onesignal_player_id = graphene.String()

    def mutate(self, info, username, password, email, onesignal_player_id=None):
        user = get_user_model()(
            username=username,
            email=email,
            onesignal_player_id=onesignal_player_id
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        username = graphene.String()
        fullName = graphene.String()
        email = graphene.String()
        gender = graphene.Int()
        about = graphene.String()
        location = graphene.List(graphene.Float)
        isOnline = graphene.Boolean()
        familyPlans = graphene.Int()
        age = graphene.Int()
        tag_ids = graphene.List(graphene.Int)
        politics = graphene.Int()
        zodiacSign = graphene.Int()
        height = graphene.Int()
        interested_in = graphene.List(graphene.Int)
        ethinicity = graphene.Int()
        religion = graphene.Int()
        education = graphene.String()
        music = graphene.List(graphene.String)
        tvShows = graphene.List(graphene.String)
        sportsTeams = graphene.List(graphene.String)
        movies = graphene.List(graphene.String)
        work = graphene.String()
        book = graphene.List(graphene.String)
        avatar = graphene.String()
        onesignal_player_id = graphene.String()
        # depricated 
        # photos = graphene.List(graphene.String)
        likes = graphene.List(graphene.String)

        url = graphene.String()
        platform = graphene.Int(
            description="Number of social platform 1.GOOGLE 2.FACEBOOK 3.INSTAGRAM 4.SNAPCHAT 5.LINKEDIN")

    Output = userResponseObj

    def mutate(self, info, id, username=None, fullName=None, gender=None, email=None, height=None, familyPlans=None,
               about=None, location=None, age=None, avatar=None, isOnline=None, tag_ids=None, url=None, platform=None,
               politics=None, zodiacSign=None, interested_in=None, ethinicity=None, religion=None, education=None,
               photos=None, onesignal_player_id=None, music=None, likes=None, book=None, movies=None, sportsTeams=None,
               tvShows=None, work=None):
        global socialObj
        user = get_user_model().objects.get(id=id)
        try:
            profile = UserSocialProfile.objects.get(user=user)
        except:
            profile = None
        if username is not None:
            user.username = username
        if fullName is not None:
            user.fullName = fullName
        if gender is not None:
            user.gender = gender
        if email is not None:
            user.email = email
        if height is not None:
            user.height_id = height
            heightObj = Height.objects.filter(height=height).first()
            if heightObj:
                user.height = heightObj.height
        if work is not None:
            user.work = work
        if familyPlans is not None:
            user.familyPlans = familyPlans
        if about is not None:
            user.about = about
        if location is not None:
            loc = list(map(str, location))
            user.location = f'{loc[0]}, {loc[1]}'
        if age is not None:
            # user.age_id = age
            ageObj = Age.objects.filter(id=age).first()
            if ageObj:
                user.age = ageObj
        if isOnline is not None:
            user.isOnline = isOnline
        if tag_ids is not None:
            user.tags.clear()
            for tag_id in tag_ids:
                tag = tags.objects.get(id=tag_id)
                if tag is not None:
                    user.tags.add(tag)
        if politics is not None:
            user.politics = politics
        if music is not None:
            user.music.clear()
            for music_ in music:
                m, _ = Music.objects.get_or_create(
                    interest=music_,
                    defaults={'interest': music_}
                )
                user.music.add(m)
        if movies is not None:
            user.movies.clear()
            for movie_ in movies:
                m, _ = Movies.objects.get_or_create(
                    interest=movie_,
                    defaults={'interest': movie_}
                )
                user.movies.add(m)
        if sportsTeams is not None:
            user.sportsTeams.clear()
            for team in sportsTeams:
                t, _ = SportsTeams.objects.get_or_create(
                    interest=team,
                    defaults={'interest': team}
                )
                user.sportsTeams.add(t)
        if likes is not None:
            user.likes.clear()
            for user_id in likes:
                user_ = get_user_model().objects.get(id=user_id)
                if user_ is not None:
                    user.likes.add(user_)
        if book is not None:
            user.book.clear()
            for book_title in book:
                b, _ = Book.objects.get_or_create(interest=book_title,
                                                  defaults={'interest': book_title})
                user.book.add(b)
        if tvShows is not None:
            user.tvShows.clear()
            for show in tvShows:
                s, _ = TVShow.objects.get_or_create(interest=show,
                                                    defaults={'interest': show})
                user.tvShows.add(s)
        if zodiacSign is not None:
            user.zodiacSign = zodiacSign
        if interested_in is not None:
            user.interested_in = ','.join(str(i) for i in interested_in)
        if ethinicity is not None:
            user.ethinicity = ethinicity
        if religion is not None:
            user.religion = religion
        if education is not None:
            user.education = education
        if avatar is not None:
            user.avatar = avatar
        if onesignal_player_id is not None:
            user.onesignal_player_id = onesignal_player_id
        
        # depricated property
        # if photos is not None:
        #     user.photo_set.all().delete()
        #     for photo in photos:
        #         new_pic = Photo.objects.create(
        #             user=user,
        #             image_data=photo
        #         )
        #         new_pic.save()

        if url is not None or platform is not None:
            if profile is None:
                new_profile = UserSocialProfile.objects.create(url=url, platform=platform, user=user)
                new_profile.save()
            else:
                if url is not None:
                    profile.url = url
                    profile.save()
                if platform is not None:
                    profile.platform = platform
                    profile.save()
        
        user.save()
        return userResponseObj(id=user.id, username=user.username)


class DeleteProfileResponse(graphene.ObjectType):
    result = graphene.String()


class DeleteProfile(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    Output = DeleteProfileResponse

    def mutate(self, info, id):
        try:
            u = User.objects.get(id=id)
            if info.context.user.id!=u.id:
                raise GraphQLError(message="You are not authorized to delete this account")
            else:
                u.delete()
                return DeleteProfileResponse(result='Profile deleted.')
        except User.DoesNotExist:
            raise Exception('Account does not exist')


class Mutation(
    user.schema.Mutation,
    reports.schema.Mutation,
    purchase.schema.Mutation,
    chatapp.schema.Mutation,
    graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    updateProfile = UpdateProfile.Field()
    # depricated due to dangerous use case and unathenticated code
    deleteProfile = DeleteProfile.Field()


class Query(
    # travel_log_data.schema.Query,
    defaultPicker.schema.Query,
    chatapp.schema.Query,
    user.schema.Query,
    graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.String(required=True))
    random_users = graphene.List(
        UserType,
        interested_in=graphene.Int(required=True),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        id=graphene.String(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        description="Search users based on their age, interest, height or gender"
    )
    popular_users = graphene.List(
        UserType,
        interested_in=graphene.Int(required=True),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        id=graphene.String(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        description="Search users based on their age, interest, height or gender"
    )
    most_active_users = graphene.List(
        UserType,
        interested_in=graphene.Int(required=True),
        min_height=graphene.Int(),
        max_height=graphene.Int(),
        id=graphene.String(),
        limit=graphene.Int(),
        min_age=graphene.Int(),
        max_age=graphene.Int(),
        latitude=graphene.Float(),
        longitude=graphene.Float(),
        family_plan=graphene.Int(),
        max_distance=graphene.Int(),
        politics=graphene.Int(),
        religious=graphene.Int(),
        zodiacSign=graphene.Int(),
        search_key=graphene.String(),
        description="Search users based on their age, interest, height or gender"
    )

    def resolve_users(self, info):
        return get_user_model().objects.filter(Q(social_auth__isnull=False) | Q(social_auth__isnull=True))

    @staticmethod
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return get_user_model().objects.get(id=id)
        else:
            raise Exception('id is a required parameter')

    @staticmethod
    def resolve_random_users(self, info, **kwargs):
        response=[]
        interest = kwargs.get('interested_in')
        max_age = kwargs.get('max_age')
        min_age = kwargs.get('min_age')
        max_height = kwargs.get('max_height')
        min_height = kwargs.get('min_height')
        userid = kwargs.get('id')
        limit = kwargs.get('limit')
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        search_key = kwargs.get('search_key')
        family_plan = kwargs.get('family_plan')
        politics = kwargs.get('politics')
        religious = kwargs.get('religious')
        zodiacSign = kwargs.get('zodiacSign')
        max_distance = kwargs.get('max_distance')

        if interest is not None:
            users = get_user_model().objects.all()
            filtered_users = []
            for user in users:
                if interest in user.interestedIn_display:
                    filtered_users.append(user.id)
            filtered_users = list(set(filtered_users))
            res = get_user_model().objects.filter(id__in=filtered_users)

        if latitude:
            res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter( ~Q(id=userid))

        if longitude:
            res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key:
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                user_location = tuple(map(float, user.location.split(',')))
                if not user_location:
                    continue
                if geopy.distance.distance(base_location, user_location).miles <= max_distance:
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))
        if limit:
            res = res[:limit]
        return res
    @staticmethod
    def resolve_popular_users(self, info, **kwargs):
        response=[]
        interest = kwargs.get('interested_in')
        max_age = kwargs.get('max_age')
        min_age = kwargs.get('min_age')
        max_height = kwargs.get('max_height')
        min_height = kwargs.get('min_height')
        userid = kwargs.get('id')
        limit = kwargs.get('limit')
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        search_key = kwargs.get('search_key')
        family_plan = kwargs.get('family_plan')
        politics = kwargs.get('politics')
        religious = kwargs.get('religious')
        zodiacSign = kwargs.get('zodiacSign')
        max_distance = kwargs.get('max_distance')
        # userdata=User.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:limit]
        # print("userdata",userdata)
        if interest is not None:
            users = get_user_model().objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
            # print("users",users)
            filtered_users = []
            for user in users:
                if interest in user.interestedIn_display:
                    filtered_users.append(user.id)
            filtered_users = list(set(filtered_users))
            res = get_user_model().objects.filter(id__in=filtered_users)

        if latitude:
            res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter( ~Q(id=userid))
        if longitude:
            res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key:
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                user_location = tuple(map(float, user.location.split(',')))
                if not user_location:
                    continue
                if geopy.distance.distance(base_location, user_location).miles <= max_distance:
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))
        if limit:
            res = res[:limit]
        return res
    @staticmethod
    def resolve_most_active_users(self, info, **kwargs):
        response=[]
        interest = kwargs.get('interested_in')
        max_age = kwargs.get('max_age')
        min_age = kwargs.get('min_age')
        max_height = kwargs.get('max_height')
        min_height = kwargs.get('min_height')
        userid = kwargs.get('id')
        limit = kwargs.get('limit')
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        search_key = kwargs.get('search_key')
        family_plan = kwargs.get('family_plan')
        politics = kwargs.get('politics')
        religious = kwargs.get('religious')
        zodiacSign = kwargs.get('zodiacSign')
        max_distance = kwargs.get('max_distance')
        if interest is not None:
            users = get_user_model().objects.all()
            filtered_users = []
            for user in users:
                if interest in user.interestedIn_display:
                    filtered_users.append(user.id)
            filtered_users = list(set(filtered_users))
            res = get_user_model().objects.filter(id__in=filtered_users)
        if latitude:
            res = res.filter(location__contains=latitude)
        if userid:
            res = res.filter( ~Q(id=userid))
        if longitude:
            res = res.filter(location__contains=longitude)

        if family_plan:
            res = res.filter(familyPlans=family_plan)

        if politics:
            res = res.filter(politics=politics)

        if religious:
            res = res.filter(religion=religious)

        if zodiacSign:
            res = res.filter(zodiacSign=zodiacSign)

        if search_key:
            res = res.filter(fullName__contains=search_key)

        if max_distance and latitude and longitude:
            base_location = float(latitude), float(longitude)
            within_vicinity = []
            for user in res:
                user_location = tuple(map(float, user.location.split(',')))
                if not user_location:
                    continue
                if geopy.distance.distance(base_location, user_location).miles <= max_distance:
                    within_vicinity.append(user.id)
            if within_vicinity:
                res = res.filter(id__in=within_vicinity)

        if max_age is not None or min_age is not None:
            if max_age is None:
                max_age = Age.objects.last().age
            if min_age is None:
                min_age = Age.objects.first().age
            res = res.filter(age__age__range=(min_age, max_age))

        if max_height is not None or min_height is not None:
            if max_height is None:
                max_height = Height.objects.last().height
            if min_height is None:
                min_height = Height.objects.first().height

            res = res.filter(height__height__range=(min_height, max_height))
        res=res.filter(isOnline=True)
        if limit:
            res = res[:limit]
        print("res",res)
        return res
        
schema = graphene.Schema(query=Query, mutation=Mutation)
