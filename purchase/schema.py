import graphene
from graphene import *
from user.models import User
from .models import Purchase


class purchaseResponseObj(graphene.ObjectType):
    id = graphene.Int()
    coins = graphene.Int()
    success = graphene.Boolean()


class purchaseCoin(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        method = graphene.String()
        coins = graphene.Int()
        money = graphene.Float()

    Output = purchaseResponseObj

    def mutate(self, info, id, method, coins, money):
        user = User.objects.get(id=id)
        user.coins = user.coins + coins
        user.save()

        new_purchase = Purchase.objects.create(user=user, method=method, coins=coins, money=money)
        new_purchase.save()

        return purchaseResponseObj(id=new_purchase.purchase_id, coins=user.coins, success=True)


class Mutation(graphene.ObjectType):
    purchaseCoin = purchaseCoin.Field()
