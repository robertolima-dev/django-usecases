

class AccessLevelManager:

    def can_create_product(self, user, ):

        if user.profile.access_level == 'user':
            raise Exception('Sem autorização para criar produto!')
        return
