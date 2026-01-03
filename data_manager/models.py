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

class KnowledgeBase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class KnowledgeSource(models.Model):
    SOURCE_TYPES = [
        ('pdf', 'PDF'),
        ('url', 'URL'),
        ('text', 'Text'),
        ('api', 'API'),
    ]

    base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE, related_name='sources')
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    source_identifier = models.TextField()  # URL, filename, etc.
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type}: {self.source_identifier}"

class Document(models.Model): 
    """raw extracted text before chunking"""
    source = models.ForeignKey(KnowledgeSource, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Document {self.pk}"

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    index = models.PositiveIntegerField()
    text = models.TextField()
    token_count = models.PositiveIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['document', 'index']
        unique_together = ('document', 'index')

    def __str__(self):
        return f"Chunk {self.index} of Doc {self.document.pk}"