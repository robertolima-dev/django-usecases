import random

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from requests_toolbelt.multipart.encoder import MultipartEncoder
from rest_framework.authtoken.models import Token

from apps.users.api.auth.authentication import expires_in, token_expire_handler
from apps.users.api.auth.serializers import UserSerializer
from apps.users.models import Hash, Profile

UserModel = get_user_model()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserDataManager:

    def auth_user(self, signin_serializer, ):

        email = signin_serializer.data['email'].lower().strip()
        password = signin_serializer.data['password']

        try:
            user = UserModel.objects.get(email=email) # noqa501

            if user.check_password(raw_password='deafult_emannar_sync_2024'):

                url = 'https://api-nova-emannar.emannar.com/api/v1/auth/login' # noqa501
                mp_encoder = MultipartEncoder(fields={
                        'username': email,
                        'password': password,
                    })

                r = requests.post(
                    url,
                    data=mp_encoder,
                    headers={'Content-Type': mp_encoder.content_type}
                )

                if r.status_code == 200 and r.json().get('access_token'):

                    user.set_password(password)
                    user.save()

                    return self.user_is_authenticated(
                        user=user,
                        module='login'
                    )

                raise Exception('E-mail ou senha inválidos') # noqa501

            if not user or not user.is_active or not user.check_password(raw_password=password): # noqa501
                raise Exception('E-mail ou senha inválidos') # noqa501

            if user.profile.access_level != 'user':
                self.handle_onboarding_login(user=user)

            return self.user_is_authenticated(
                user=user,
                module='login'
            )

        except UserModel.DoesNotExist:
            raise Exception('E-mail ou senha inválidos') # noqa501

    def user_is_authenticated(self, user, module, ):

        token, _ = Token.objects.get_or_create(user=user)

        is_expired, token = token_expire_handler(token) # noqa501
        user_serialized = UserSerializer(user)

        response = {
            'user': user_serialized.data,
            'expires_in': expires_in(token),
            'token': token.key
        }

        return response, user

    def register_user(self, request):

        try:

            if len(request.data.get('name').split(' ')) == 1:
                raise Exception('Nome e sobrenome é obrigatório')

            email = request.data.get('email').lower().strip()

            user = UserModel.objects.filter(
                email=email
                ).first()

            if user:
                raise Exception('Usuário já cadastrado')

            UserModel.objects.create_user(
                email=email,
                username=f"{request.data.get('name').replace(' ', '').lower().strip()}_{str(random.randrange(99))}", # noqa501
                password=request.data.get('password'),
                first_name=request.data.get('name').split(' ')[0],
                last_name=request.data.get('name').split(' ')[1] if len(request.data.get('name').split(' ')) > 1 else '' # noqa501
            )

            user = UserModel.objects.get(email=email) # noqa501

            # invite = Invite.objects.filter(
            #    email_invited=email
            # ).first()

            # if invite:
            #     invite.registered = True
            #     invite.save()

            return self.user_is_authenticated(
                user=user,
                module='register'
            )

        except UserModel.DoesNotExist:
            raise Exception('E-mail ou senha inválidos') # noqa501

    def html_new_user(self, user, ):
        html: any = """
                <div style="max-width: 600px; background: rgba(245, 245, 245, 1); margin: auto;">
                    <div style="background: #417b74; width: 100%; height: 92px; padding-top: 22px;">
                        <img src="{project_image}"  alt="next_intake" style="display: block; margin-left: auto; margin-right: auto; width: 70px; margin: auto;"/>
                    </div>
                    <div style="padding: 40px;">

                        <div style="margin-top: 24px; color: rgba(0, 0, 0, 1); font-size: 14px; font-weight: 400;">
                            Novo user
                        </div>
                        <div style="margin-top: 24px; color: rgba(0, 0, 0, 1); font-size: 14px; font-weight: 400;">
                            User: {email}
                        </div>

                    </div>
                </div>
            """.format(  # noqa: E501
                project_image=settings.PROJECT_IMAGE,
                email=user.email,
                )
        return html

    def confirm_email_user(self, hash):

        hash_data = Hash.objects.filter(
            hash=hash
            ).first()

        if not hash_data:
            raise Exception('Token inválido')

        Profile.objects.filter(
            user=hash_data.user
        ).update(
            confirm_email=True
        )

        # hash_data.delete()

        return

    def forgot_password_user(self, email):

        user = UserModel.objects.filter(email=email).first()

        if not user:
            raise Exception('Usuário não encontrado')

        hash_change_password, created = Hash.objects.get_or_create(
            user=user,
            type='change_password'
            )

        return

    def change_password_user(self, hash, jwt, new_password):

        if not hash and not jwt:
            raise Exception('Token é obrigatório')

        if hash:
            hash_change_password = Hash.objects.filter(
                hash=hash,
                type='change_password'
                ).first()

            if not hash_change_password:
                raise Exception('Token não encontrado')

            user = UserModel.objects.filter(
                id=hash_change_password.user_id
            ).first()

        if jwt:
            url = 'https://api-nova-emannar.emannar.com/api/v1/auth/me' # noqa501
            headers = {'Authorization': 'Bearer ' + jwt}

            r = requests.get(
                url,
                headers=headers
            )

            if r.status_code != 200:
                raise Exception('Usuário não autenticado')

            user = UserModel.objects.filter(
                email=r.json().get('email')
                ).first()

        if not user:
            raise Exception('Usuário não encontrado')

        user.set_password(new_password)
        user.save()

        if hash:
            hash_change_password.delete()

        return self.user_is_authenticated(
            user=user,
            module='login'
        )

    def unsubscribe_user(self, hash, unsubscribe):

        hash_data = Hash.objects.filter(
            hash=hash,
            type='unsubscribe'
        ).first()

        if not hash_data:
            raise Exception('Token não encontrado')

        user = UserModel.objects.filter(
            id=hash_data.user_id
            ).first()

        if not user:
            raise Exception('Usuário não encontrado')

        Profile.objects.filter(
            user_id=user.id
        ).update(
            unsubscribe=unsubscribe
        )

        return

    def delete_user(self, user, ):

        instance = User.objects.filter(
            id=user.id
        ).first()

        instance.is_active = False
        instance.save()

        return
