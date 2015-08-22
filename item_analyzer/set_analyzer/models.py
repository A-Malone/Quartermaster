from django.db import models

#SQLite Models


#Mongo Models
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, IntField, BooleanField, DateTimeField
from mongoengine import ReferenceField, ListField, DictField, EmbeddedDocumentField

#----Champion Document
#----------------------------------------
class Champion(Document):
    champion_id = IntField()
    name = StringField(max_length=100)

    @classmethod
    def from_dict(cls, data):

        # Champions should be unique, so check to see if one exists already
        champ = Champion.objects(
            champion_id = int(data['id'])
        ).first()

        if(champ):
            return champ

        return Champion(
            champion_id = int(data['id']),
            name = data['name']
        )

#----Item Document
#----------------------------------------
class Item(Document):
    item_id = IntField()
    name = StringField(max_length=100)
    gold = DictField()
    stats = DictField()

    @classmethod
    def from_dict(cls, data):
        # Items should be unique, so check to see if one exists already
        item = Item.objects(
            item_id = int(data['id'])
        ).first()

        if(item):
            return item

        return Item(
            item_id = int(data['id']),
            name = data['name'],
            gold = data['gold'],
            stats = data['stats']
        )

#----Game Document
#----------------------------------------
class ItemPurchaseEvent(EmbeddedDocument):
    timestamp = IntField()
    item = ReferenceField(Item)

class ParticipantDataFrame(EmbeddedDocument):
    timestamp = IntField()
    current_gold = IntField()
    level = IntField()
    minions_killed = IntField()
    xp = IntField()

class Participant(EmbeddedDocument):
    participant_id = IntField()
    champion = ReferenceField(Champion)
    frame_data = ListField(EmbeddedDocumentField(ParticipantDataFrame))
    item_purchases = ListField(EmbeddedDocumentField(ItemPurchaseEvent))

class Team(EmbeddedDocument):
    team_id = IntField()
    won = BooleanField(required=True)
    players = ListField(EmbeddedDocumentField(Participant))

class Match(Document):
    match_id = IntField()
    teams = ListField(EmbeddedDocumentField(Team))
