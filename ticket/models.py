from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from .utils import (TICKET_PRIORITY_CHOICES, 
                    TICKET_DEPARTMENT_CHOICES, 
                    TICKET_STATUS_CHOICES,
                    size_limit)
from .utils import MEDIUM, TECHNICAL, OPEN
from django.utils.safestring import mark_safe


class Ticket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(verbose_name="عنوان", max_length=50)
    priority = models.CharField(verbose_name="اولویت", choices=TICKET_PRIORITY_CHOICES, \
                                default=MEDIUM, max_length=1)
    department = models.CharField(verbose_name="بخش", choices=TICKET_DEPARTMENT_CHOICES, \
                                default=TECHNICAL, max_length=1)
    status = models.CharField(verbose_name="وضعیت", choices=TICKET_STATUS_CHOICES, \
                                default=OPEN, max_length=1)
    date_created = jmodels.jDateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    def get_date_created(self):
        return self.date_created.strftime("%Y/%m/%d ساعت %H:%M")
    get_date_created.short_description = 'تاریخ ایجاد'

    @property
    def get_priority(self):
        return dict(TICKET_PRIORITY_CHOICES)[self.priority]

    @get_priority.setter
    def get_priority(self, priority_type):
        reversed_types = {v: k for k, v in dict(TICKET_PRIORITY_CHOICES).items()}
        self.priority = reversed_types.get(priority_type)

    @property
    def get_department(self):
        return dict(TICKET_DEPARTMENT_CHOICES)[self.department]

    @get_department.setter
    def get_department(self, department_type):
        reversed_types = {v: k for k, v in dict(TICKET_DEPARTMENT_CHOICES).items()}
        self.department = reversed_types.get(department_type)

    @property
    def get_status(self):
        return dict(TICKET_STATUS_CHOICES)[self.status]

    @get_status.setter
    def get_status(self, status_type):
        reversed_types = {v: k for k, v in dict(TICKET_STATUS_CHOICES).items()}
        self.status = reversed_types.get(status_type)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.title}"

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = '  تیکت‌ها'
        ordering = ['-date_created']



class Message(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, verbose_name="تیکت")
    admin_reply = models.BooleanField(verbose_name="پاسخ ادمین", default=False)
    is_seen = models.BooleanField(verbose_name="خوانده‌شده", default=False)
    date_sent = jmodels.jDateTimeField(verbose_name="تاریخ ارسال", auto_now_add=True)
    body = models.TextField(verbose_name="متن پیام")

    def get_date_sent(self):
        return self.date_sent.strftime("%Y/%m/%d ساعت %H:%M")
    get_date_sent.short_description = 'تاریخ ارسال'

    def __str__(self) -> str:
        if self.admin_reply:
            return f"پیام مدیر در تاریخ {self.get_date_sent()}"
        return f"{self.ticket.user.get_full_name()} در تاریخ {self.get_date_sent()}"

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = ' پیام‌ها'
        ordering = ['-date_sent']


class AttachmentFiles(models.Model):
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE, verbose_name="پیام")
    image = models.ImageField(verbose_name="تصویر", validators=[size_limit], upload_to='ticket-files/images/')

    def get_image(self):
        return mark_safe('<img src="{}" width="100" height="100">'.format("/media/" + str(self.image)))
    get_image.short_description = 'تصویر'

    class Meta:
        verbose_name = 'فایل ضمیمه‌شده'
        verbose_name_plural = 'فایل‌های ضمیمه‌شده'