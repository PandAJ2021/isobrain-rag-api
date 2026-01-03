from django.db import models
from django.conf import settings
from tenants.models import Client


class TenantUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tenants')
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('member', 'Member')])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'tenant'], name='unique_tenant_user'),
        ]
    def __str__(self):
        return f"{self.user} → {self.tenant} ({self.role})"
