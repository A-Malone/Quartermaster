from django.db import models

#SQLite Models


#Mongo Models
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, IntField, BooleanField, DateTimeField
from mongoengine import ReferenceField, ListField, DictField, EmbeddedDocumentField, MapField

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
    version = StringField(max_length=50)
    name = StringField(max_length=100)
    gold = DictField()
    stats = DictField()

    @classmethod
    def from_dict(cls, data):
        # Items should be unique, so check to see if one exists already
        item = Item.objects(
            item_id = int(data['id']),
            version = data['version']
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
class ItemEvent(EmbeddedDocument):
    timestamp = IntField()
    event_type = StringField(max_length=50)

    payload = DictField()

    @classmethod
    def from_dict(cls, data):
        item_event =  ItemEvent(
            timestamp = data['timestamp'],
            event_type = data['eventType'],
            payload = data
        )
        item_event.save()
        return item_event

class ParticipantDataFrame(EmbeddedDocument):
    timestamp = IntField()
    current_gold = IntField()
    total_gold = IntField()
    level = IntField()
    minions_killed = IntField()
    xp = IntField()

    @classmethod
    def from_dict(cls, data):
        pdf = ParticipantDataFrame(
            current_gold=data['currentGold'],
            total_gold=data['totalGold'],
            level=data['level'],
            minions_killed = data['minionsKilled'],
            xp=data['xp'],
            team_score=data['teamScore']
        )
        pdf.save()
        return pdf

class Participant(EmbeddedDocument):
    participant_id = IntField()
    team_id = IntField()
    champion = ReferenceField(Champion)
    frame_data = ListField(EmbeddedDocumentField(ParticipantDataFrame))
    item_events = ListField(EmbeddedDocumentField(ItemEvent))

    @classmethod
    def from_dict(cls, data):
        part =  Participant(
            participant_id = data['participantId'],
            team_id = data['teamId'],
            champion =  Champion.objects(champion_id=data['championId']).get()
        )
        part.save()
        return part

class Team(EmbeddedDocument):
    won = BooleanField(required=True)
    @classmethod
    def from_dict(cls, data):
        team = Team(
            won = data['winner']
        )
        team.save()
        return team


class Match(Document):
    match_id = IntField()
    version = StringField(max_length=50)

    teams = MapField(field=EmbeddedDocumentField(Team))
    participants = MapField(field=EmbeddedDocumentField(Participant))

    @classmethod
    def from_dict(cls, data):
        match = Match(
            match_id = int(data['matchId']),
        )

        #Parse teams
        for team_dict in data['teams']:
            team = Team.from_dict(team_dict)
            match.teams[team.team_id] = team
        match.save()

        #Parse participants
        for participant_dict in data['participants']:
            participant = Participant.from_dict(participant_dict)
            match.participants[participant.participant_id] = participant
        match.save()

        #Parse frame events
        for frame_dict in data['frames']:
            ts = int(frame_dict['timestamp'])
            for pid, participant_frame_dict in frame_dict['participantFrames'].items():
                pdf = ParticipantDataFrame.from_dict(participant_frame_dict)
                pdf.timestamp = ts
                pdf.save()
                participant = match.participants[participant_id]
                participant.frame_data.append(pdf)
                participant.save()

            for event_dict in  frame_dict['events']:
                if(event_dict['evenType'].startswith("ITEM")):
                    item_event = ItemEvent.from_dict(event_dict)
                    participant = match.participants[event_dict['participantId']]
                    participant.item_events.append(item_event)
                    participant.save()

        return match
