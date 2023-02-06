from django.db import models


class EmailHistory(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="email_history")
    success = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = "Email History"
