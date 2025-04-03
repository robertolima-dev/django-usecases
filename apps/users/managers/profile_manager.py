from django.contrib.auth import get_user_model

from apps.users.models import Profile

UserModel = get_user_model()


class ProfileManager:

    def create_or_update_profile(self, user, profile_serializer, ):

        profile = Profile.objects.filter(
            user=user
        ).first()

        if not profile:
            Profile.objects.create(
                user=user,
                bio=profile_serializer.data.get('bio', None),
                birth_date=profile_serializer.data.get('birth_date', None),
                phone=profile_serializer.data.get('phone', None),
                profession=profile_serializer.data.get('profession', None),
                document=profile_serializer.data.get('document', None),
                avatar=profile_serializer.data.get('avatar', None),
                address=profile_serializer.data.get('address', None),
            )

        else:
            if profile_serializer.data.get('bio'):
                profile.bio = profile_serializer.data['bio']
            if profile_serializer.data.get('location'):
                profile.location = profile_serializer.data['location']
            if profile_serializer.data.get('birth_date'):
                profile.birth_date = profile_serializer.data['birth_date']
            if profile_serializer.data.get('profession'):
                profile.profession = profile_serializer.data['profession']
            if profile_serializer.data.get('phone'):
                profile.phone = profile_serializer.data['phone']
            if profile_serializer.data.get('document'):
                profile.document = profile_serializer.data['document']
            if profile_serializer.data.get('avatar'):
                profile.avatar = profile_serializer.data['avatar']
            if profile_serializer.data.get('address'):
                profile.address = profile_serializer.data['address']

            profile.save()

        return

    def change_access_level(self, user, ):

        instance = Profile.objects.get(
            user=user
        )

        if instance and instance.access_level == 'user':
            instance.access_level = 'professional_free'
            instance.save()

        return instance
