from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget

from apps.mailer.tasks import send_email

from .models import EmailLog, EmailTemplate


@admin.action(description="Reenviar email")
def resend_email(modeladmin, request, queryset):
    for instance in queryset:
        send_email.delay(
            recipient=instance.recipient,
            template_name=instance.template.name,
            context=instance.context
        )


@admin.register(EmailTemplate)
class EmailTemplateAdmin(SummernoteModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': SummernoteWidget},
    }
    list_display = ('name', 'subject', 'created_at', 'updated_at')
    search_fields = ('name', 'subject')
    list_filter = ('created_at', 'updated_at')


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'status', 'created_at')
    search_fields = ('recipient', 'subject')
    list_filter = ('status', 'created_at')
    actions = [
        resend_email,
    ]
