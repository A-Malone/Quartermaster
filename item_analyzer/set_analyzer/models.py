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

    build_from = ListField(IntField())
    build_into = ListField(IntField())

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
            stats = data['stats'],
            version = data['version'],
            build_from = data.get('from', []),
            build_into = data.get('into', [])
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
        return item_event

class ParticipantDataFrame(EmbeddedDocument):
    timestamp = IntField()
    current_gold = IntField()
    total_gold = IntField()
    level = IntField()
    minions_killed = IntField()
    xp = IntField()
    team_score = IntField()

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
        return pdf

class Participant(EmbeddedDocument):
    participant_id = IntField()
    team_id = IntField()
    champion = ReferenceField(Champion)
    frame_data = ListField(EmbeddedDocumentField(ParticipantDataFrame))
    item_events = ListField(EmbeddedDocumentField(ItemEvent))
    final_build = ListField(IntField())

    #Model stats
    kills = IntField()
    deaths = IntField()
    assists = IntField()
    gold_earned = IntField()

    @classmethod
    def from_dict(cls, data):
        part =  Participant(
            participant_id = data['participantId'],
            team_id = data['teamId'],
            champion =  Champion.objects(
                champion_id=int(data['championId']
                )
            ).get(),
            kills = data['stats']['kills'],
            deaths = data['stats']['deaths'],
            assists = data['stats']['assists'],
            gold_earned = data['stats']['goldEarned'],
            final_build = [data['stats'].get("item{}".format(x), None) for x in range(7)]
        )
        return part

class Team(EmbeddedDocument):
    team_id = IntField()
    won = BooleanField(required=True)
    @classmethod
    def from_dict(cls, data):
        team = Team(
            team_id = data['teamId'],
            won = data['winner']
        )
        return team

class Match(Document):
    match_id = IntField()
    version = StringField(max_length=50)
    duration = IntField()

    teams = MapField(field=EmbeddedDocumentField(Team))
    participants = MapField(field=EmbeddedDocumentField(Participant))

    @classmethod
    def from_dict(cls, data):
        match = Match(
            match_id = int(data['matchId']),
            duration = data['matchDuration'],
            version = data['matchVersion']
        )

        #Parse teams
        for team_dict in data['teams']:
            team = Team.from_dict(team_dict)
            match.teams[str(team.team_id)] = team
        match.save()

        #Parse participants
        for participant_dict in data['participants']:
            participant = Participant.from_dict(participant_dict)
            match.participants[str(participant.participant_id)] = participant
        match.save()

        #Parse frame events
        for frame_dict in data['timeline']['frames']:
            ts = int(frame_dict['timestamp'])
            if('participantFrames' in frame_dict):
                for pid, participant_frame_dict in frame_dict['participantFrames'].items():
                    pdf = ParticipantDataFrame.from_dict(participant_frame_dict)
                    pdf.timestamp = ts
                    participant = match.participants[pid]
                    participant.frame_data.append(pdf)
            if('events' in frame_dict):
                for event_dict in  frame_dict['events']:
                    if(event_dict['eventType'].startswith("ITEM")):
                        if(int(event_dict['participantId'])):
                            item_event = ItemEvent.from_dict(event_dict)
                            participant = match.participants[str(event_dict['participantId'])]
                            participant.item_events.append(item_event)
        match.save()


        return match
