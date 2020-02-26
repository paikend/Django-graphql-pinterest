import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import superuser_required
from accounts.models import User , UserProfile

# type CreateUserPayload {
#   ok: Boolean
#   actor: Actor
# }
class UserModelType(DjangoObjectType):
    class Meta:
        model = User
    def resolve_viewer(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        return user
class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile

class Query(object):
    all_users = graphene.List(UserModelType)
    all_user_profiles = graphene.List(UserProfileType)
    user = graphene.Field(UserModelType, id=graphene.Int())
    user_profile = graphene.Field(UserProfileType, id=graphene.Int())
    @superuser_required
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(id=id)
        return None
    @superuser_required
    def resolve_all_user_profiless(self, info, **kwargs):
        return UserProfile.objects.all()
    def resolve_user_profile(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return UserProfile.objects.get(id=id)
        return None



class CreateGeneralUser(graphene.Mutation):
    user = graphene.Field(UserModelType)
    ok = graphene.Boolean()
    class Arguments:
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        ok = True
        user = User.objects._create_user(
            email=kwargs.get('email'),
            type='g',
            password=kwargs.get('password')
        )
        return CreateGeneralUser(ok=ok, user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateGeneralUser.Field()