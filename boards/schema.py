import graphene
from graphql_jwt.decorators import login_required
from django.conf import settings
from graphene_django.types import DjangoObjectType

from boards.models import Board, Section, Pin
from django.shortcuts import resolve_url
from graphene_file_upload.scalars import Upload

class PinType(DjangoObjectType):
    class Meta:
        model = Pin
    photo_url = graphene.String()

    def resolve_photo_url(self, info):
        return info.context.build_absolute_uri(self.photo.url)
class CreatePin(graphene.Mutation):
    pin = graphene.Field(PinType)
    ok = graphene.Boolean()
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        related_link = graphene.String()
        photo = Upload(required=True)
    def mutate(root, info, photo, **kwargs):
        ok = True
        pin = Pin(
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            related_link=kwargs.get('related_link'),
            photo = photo
        )
        pin.save()
        return CreatePin(ok=ok, pin=pin)
class UpdatePin(graphene.Mutation):
    pin = graphene.Field(PinType)
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        photo = Upload()
    def mutate(root, info, photo,  **kwargs):
        pin = Pin.objects.get(id=kwargs.get('id'))
        if pin:
            ok = True
            pin.title = kwargs.get('title')
            pin.description = kwargs.get('description')
            pin.photo = photo
            pin.save()
        return UpdatePin(ok=ok, pin=pin)
class DeletePin(graphene.Mutation):
    pin = graphene.Field(PinType)
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()

    def mutate(root, info, **kwargs):
        ok = True
        pin = Pin.objects.get(id=kwargs.get('id'))
        pin.delete()
        return UpdateBoard(ok=ok, pin=pin)
class BoardType(DjangoObjectType):
    class Meta:
        model = Board
class CreateBoard(graphene.Mutation):
    board = graphene.Field(BoardType)
    ok = graphene.Boolean()
    class Arguments:
        name = graphene.String()
        description = graphene.String()
    def mutate(root, info, **kwargs):
        ok = True
        board = Board(
            name = kwargs.get('name'),
            description = kwargs.get('description'),
        )
        board.save()
        return CreateBoard(ok=ok, board=board)
class UpdateBoard(graphene.Mutation):
    board = graphene.Field(BoardType)
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
    def mutate(root, info, **kwargs):
        board = Board.objects.get(id=kwargs.get('id'))
        if board:
            ok = True
            board.name = kwargs.get('name')
            board.description = kwargs.get('description')
            board.save()
        return UpdateBoard(ok=ok, board=board)

class DeleteBoard(graphene.Mutation):
    board = graphene.Field(BoardType)
    ok = graphene.Boolean()
    class Arguments:
        id = graphene.ID()

    def mutate(root, info, **kwargs):
        board = Board.objects.get(id=kwargs.get('id'))
        if board:
            ok = True
            board.delete()
        return UpdateBoard(ok=ok, board=board)
class SectionType(DjangoObjectType):
    class Meta:
        model = Section

import json
# from django.urls import reverse
class Query(object):
    all_pins = graphene.List(PinType)
    pin = graphene.Field(PinType, id=graphene.Int())
    all_boards = graphene.List(BoardType)
    board = graphene.Field(BoardType, id=graphene.Int())
    all_sections = graphene.List(SectionType)
    section = graphene.Field(SectionType, id=graphene.Int())


    # @login_required
    def resolve_all_pins(self, info, **kwargs):
        return Pin.objects.all().order_by('id')
    def resolve_all_sections(self, info, **kwargs):
        return Section.objects.all()
    def resolve_all_boards(self, info, **kwargs):
        return  Board.objects.all()
    def resolve_pin(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Pin.objects.get(id=id)
        return None
    def resolve_board(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Board.objects.get(id=id)
        return None
    def resolve_section(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Section.objects.get(id=id)
        return None
# class Mutations
class Mutation(graphene.ObjectType):
    create_board = CreateBoard.Field()
    update_board = UpdateBoard.Field()
    delete_board = DeleteBoard.Field()
    create_pin = CreatePin.Field()
    update_pin = UpdatePin.Field()
    delete_pin = DeletePin.Field()