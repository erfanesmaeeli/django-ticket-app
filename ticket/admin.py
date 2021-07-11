from django.contrib import admin
from .models import Ticket, Message, AttachmentFiles

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ['user', 'title', 'department', 'priority', 'status', 'get_date_created', 'id']
	list_editable = ['status']
	list_filter = ['department', 'priority', 'status', 'user']
	search_fields = ['user__username', 'user__first_name', 'user__last_name', 'title']
	readonly_fields = ['user', 'title']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['ticket', 'admin_reply', 'is_seen', 'get_date_sent']
	list_filter = ['admin_reply', 'is_seen']
	search_fields = ['body', 'ticket__user__username', 'ticket__user__first_name', 'ticket__user__last_name']
	readonly_fields = ['body']


@admin.register(AttachmentFiles)
class AttachmentFilesAdmin(admin.ModelAdmin):
	list_display = ['message', 'image']
	list_filter = ['message']