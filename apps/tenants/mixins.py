class TenantQuerysetMixin:
    """
    Mixin para isolar os dados por tenant de forma automática.
    Usa request.tenant (injetado pelo middleware).
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = getattr(self.request, 'tenant', None)

        if tenant is not None:
            return queryset.filter(tenant=tenant)

        return queryset.none()  # evita vazar dados se tenant não for resolvido
