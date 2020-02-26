import graphene

import boards.schema
import accounts.schema
import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug



class Query(boards.schema.Query, accounts.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    sdebug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(accounts.schema.Mutation, boards.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)