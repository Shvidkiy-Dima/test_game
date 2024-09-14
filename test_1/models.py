from decimal import Decimal

from django.utils import timezone

from django.db import models




class Player(models.Model):
    first_entry = models.DateTimeField(editable=False)
    points = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )


class PlayerBoost(models.Model):
    pass

class Boost(models.Model):

    class BoostType(models.TextChoices):
        SOME_TYPE_1 = 'SOME_TYPE_1'
        SOME_TYPE_2 = 'SOME_TYPE_2'

    name = models.CharField(max_length=124)
    boost_type = models.CharField(choices=BoostType.choices, max_length=10, default=BoostType.SOME_TYPE_1)
    player = models.ForeignKey('Player', on_delete=models.PROTECT, related_name='boosts')
    is_manual = models.BooleanField(default=True)