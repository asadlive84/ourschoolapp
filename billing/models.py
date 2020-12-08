from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class BillType(models.TextChoices):
    DEBIT = 'DB', _('Debit')
    CREDIT = 'CR', _('CREDIT')


class BillingMainTitle(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name="bill_title_created")
    is_approved_first = models.BooleanField(default=False)
    is_approved_second = models.BooleanField(default=False)

    is_approved_by_second_first = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                    on_delete=models.PROTECT,
                                                    related_name="billing_main_title_approve_first",
                                                    null=True,
                                                    blank=True)
    is_approved_by_second = models.ForeignKey(settings.AUTH_USER_MODEL,
                                              on_delete=models.PROTECT,
                                              null=True,
                                              blank=True,
                                              related_name="billing_main_title_approve_second")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved_by_first_created = models.DateTimeField(null=True, blank=True)
    is_approved_by_second_created = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()


class BillingSecondTitle(models.Model):
    main_title = models.ForeignKey(BillingMainTitle, related_name="bill_main_title", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_approved_first = models.BooleanField(default=False)
    is_approved_second = models.BooleanField(default=False)

    is_approved_by_second_first = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                    on_delete=models.PROTECT,
                                                    related_name="billing_second_title_approve_first",
                                                    null=True,
                                                    blank=True)
    is_approved_by_second = models.ForeignKey(settings.AUTH_USER_MODEL,
                                              on_delete=models.PROTECT,
                                              null=True,
                                              blank=True,
                                              related_name="billing_second_second_approve_first")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved_by_first_created = models.DateTimeField(null=True, blank=True)
    is_approved_by_second_created = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()


class BillingOrder(models.Model):
    bill_type = models.CharField(
        max_length=2,
        choices=BillType.choices,
        default=BillType.DEBIT,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name="billing_order_create")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                   related_name="billing_order_updated")

    is_approved_first = models.BooleanField(default=False)
    is_approved_second = models.BooleanField(default=False)

    is_approved_by_second_first = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                    on_delete=models.PROTECT,
                                                    related_name="billing_order_approve_first",
                                                    null=True,
                                                    blank=True)
    is_approved_by_second = models.ForeignKey(settings.AUTH_USER_MODEL,
                                              on_delete=models.PROTECT,
                                              null=True,
                                              blank=True,
                                              related_name="billing_order_approve_second")

    created_at = models.DateTimeField(auto_now_add=True)
    is_donation = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.FloatField(default=0, blank=True, null=True)
    is_approved_by_first_created = models.DateTimeField(null=True, blank=True)
    is_approved_by_second_created = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()


class BillingOrderLine(models.Model):
    bill = models.ForeignKey(BillingOrder, on_delete=models.CASCADE, related_name="billing_order_line")
    bill_title = models.ManyToManyField(BillingSecondTitle)
    amount = models.FloatField(default=0)
