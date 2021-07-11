from django.core.exceptions import ValidationError


HIGH = 'h'
MEDIUM = 'm'
LOW = 'l'

TECHNICAL = 't'
FINANCE = 'f'
OTHER = 'o' #for Comments and suggestions

OPEN = 'o'
PENDING = 'p'
CLOSED = 'c'


TICKET_PRIORITY_CHOICES = [
	(HIGH, "زیاد"),
	(MEDIUM, "متوسط"),
	(LOW, "کم"),
]


TICKET_DEPARTMENT_CHOICES = [
	(TECHNICAL, "فنی"),
	(FINANCE, "مالی"),
	(OTHER, "نظر و پیشنهادات"),
]

TICKET_STATUS_CHOICES = [
	(OPEN, "باز"),
	(PENDING, "در حال بررسی"),
	(CLOSED, "بسته شده"),
]

# 2.5MB - 2621440
def size_limit(file):
	if file.size > 2621440:
		raise ValidationError(_('حجم فایل انتخابی بیش از 2.5 مگابایت است!'), code='invalid')
