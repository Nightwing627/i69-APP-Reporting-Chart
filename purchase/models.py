from django.db import models
from user.models import User
# Create your models here.

class Purchase(models.Model):
    purchase_id = models.BigAutoField(primary_key=True,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    method = models.CharField(max_length=255)
    coins = models.IntegerField()
    money = models.DecimalField(max_digits = 5,decimal_places = 2)

    class Meta:
        verbose_name_plural = "Purchase"
        verbose_name = "Purchase"


    def __str__(self):
        return str(self.method) + ' - ' + str(self.money) + ' ---- ' + str(self.coins)