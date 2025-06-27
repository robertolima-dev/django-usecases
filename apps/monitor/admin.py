from django.contrib import admin
from django_celery_results.models import TaskResult

admin.site.unregister(TaskResult)


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'status', 'date_created', 'date_done', 'worker',)  # noqa: E501
    list_filter = ('status', 'task_name', 'date_created')
    search_fields = ('task_id', 'task_name', 'result', 'traceback')
    readonly_fields = [f.name for f in TaskResult._meta.fields]
    ordering = ['-date_created']

    def get_runtime(self, obj):
        if obj.date_done and obj.date_created:
            delta = obj.date_done - obj.date_created
            return str(delta)
        return "-"

    get_runtime.short_description = "Runtime"
