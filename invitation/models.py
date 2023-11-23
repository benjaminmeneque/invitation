# invitations/models.py
from django.db import models
from django.utils.timezone import localtime


class Invitation(models.Model):
    COMPANY_CHOICES = [
        ("WSI", "WeSupport Inc."),
        ("HHI", "Hunters Hub Inc."),
        ("PSI", "Provisor Solutions Inc."),
        ("ESI", "Ekkremis Solutions Inc."),
        ("UpTC", "Uptitude Training Corp."),
        ("WGCCC", "WeSupport Group of Company Credit Cooperative"),
        ("TSTC", "Tranzend Solutions and Trading Corp."),
    ]

    full_name = models.CharField(max_length=100, blank=False, null=False)
    company = models.CharField(
        max_length=20, choices=COMPANY_CHOICES, blank=False, null=False
    )
    email = models.EmailField(blank=False, null=False)
    created_at = models.DateTimeField(default=localtime)
    code = models.CharField(
        max_length=15, default="WGC-0"
    )  # Assuming the code is a CharField
    phone_number = models.CharField(max_length=12, blank=False, null=False)

    @classmethod
    def increment_code(cls):
        latest_invitation = cls.objects.order_by("-id").first()
        new_id = latest_invitation.id + 1 if latest_invitation else 1
        new_code = f"WGC-{new_id}"

        return new_code

    def __str__(self):
        return f"{self.company} -{self.full_name}"
