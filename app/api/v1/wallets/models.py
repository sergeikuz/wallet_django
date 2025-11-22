import uuid
from django.db import models


class Wallet(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return str(self.uuid)

