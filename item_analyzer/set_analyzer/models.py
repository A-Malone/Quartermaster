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
    champion_name = StringField(max_length=50)

#----Item Document
#----------------------------------------
class Item(Document):
    item_id = IntField()
    item_name = StringField(max_length=50)

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

class Game(Document):
    match_id = IntField()
    teams = ListField(EmbeddedDocumentField(Team))
