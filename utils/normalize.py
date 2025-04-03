

def get_path_by_module(module: str, module_id: any, ) -> str:

    if module == 'payment':
        return ''

    elif module == 'event':
        if not module_id:
            return '/eventos'
        return '/detalhe/evento/' + str(module_id) + '/'

    elif module == 'course':
        if not module_id:
            return '/cursos'
        return '/detalhe/curso/' + str(module_id) + '/'

    elif module == 'appointment':
        if not module_id:
            return '/atendimento'
        return '/detalhe/atendimentos/' + str(module_id) + '/'

    elif module == 'goal':
        return '/metas/'

    elif module == 'professional':
        return '/profissionais/'

    elif module == 'community':
        return 'teste'

    elif module == 'calendar':
        return '/calendario/'

    elif module == 'notification':
        return '/notificacao/'

    elif module == 'profile':
        return '/perfil/'

    elif module == 'auth':
        return ''
