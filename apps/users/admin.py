from django.contrib import admin

from apps.users.models import AddressUser, Hash, Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'birth_date', 'phone',
        'document', 'avatar',
        'confirm_email', 'unsubscribe',
        'access_level',
    )
    fields = [
        'id', 'user', 'birth_date', 'phone',
        'document', 'avatar',
        'confirm_email', 'unsubscribe',
        'access_level',
    ]
    readonly_fields = (
        'id', 'user', 'dt_created',
    )
    ordering = ['-dt_created', ]
    search_fields = [
        'id',
        'access_level',
        'user__email',
    ]


# Register your models here.
@admin.register(Hash)
class HashAdmin(admin.ModelAdmin):
    list_display = (
        'hash', 'user', 'type', 'created',
    )
    fields = [
        'hash', 'user', 'type', 'created',
    ]
    readonly_fields = (
        'created',
    )
    ordering = ['-created', ]
    search_fields = [
        'user__email',
        'type'
    ]


@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'street', 'number',
        'zipcode', 'neighborhood', 'city',
        'state', 'active',
    )
    fields = [
        'id', 'user', 'street', 'number',
        'zipcode', 'neighborhood', 'city',
        'state', 'active',
    ]
    readonly_fields = (
        'id',
    )
    ordering = ['-id', ]
    search_fields = [
        'user__email',
    ]
