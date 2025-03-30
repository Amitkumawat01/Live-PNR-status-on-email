from django.db import models
from django.core.validators import RegexValidator

class EmailPNRStatus(models.Model):
    email = models.EmailField()
    pnr = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='PNR must be a 10-digit number.',
                code='invalid_pnr'
            )
        ]
    )
    isWL = models.CharField(max_length=3)
    chartstatus = models.CharField(max_length=20)

    currentStatusDetails1 = models.CharField(max_length=20) 
    currentStatusDetails2 = models.CharField(max_length=20, blank=True, null=True)
    currentStatusDetails3 = models.CharField(max_length=20, blank=True, null=True)
    currentStatusDetails4 = models.CharField(max_length=20, blank=True, null=True)
    currentStatusDetails5 = models.CharField(max_length=20, blank=True, null=True)
    currentStatusDetails6 = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
        unique_together = ['email', 'pnr']
        verbose_name = "Email PNR Status"
        verbose_name_plural = "Email PNR Statuses"

    def __str__(self):
        return f"{self.email} - {self.pnr}"