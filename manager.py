# Comp Manager Orchestrator

from collections import Counter
from collections.abc import Iterable
from typing import Generic, Optional, Union
from dataclasses import dataclass
from enum import Enum

@dataclass
class Judge:
    name: str

@dataclass
class Competitor:
    """A unique competitor"""
    name: str
    email: Optional[str]
    phone: Optional[str]

@dataclass
class Couple:
    """A unique dance pair (lead, follow) that is assigned a number"""
    number: int # an interesting question here is if we expect each couple to be only assigned one number or multiple? How do we handle multiple comps with the same couple?
    lead: Competitor
    follow: Competitor

class DanceStyle(Enum): # maybe use str enum here?
    OTHER = "OTHER"
    WALTZ = "WALTZ"
    # TODO add more styles here

class DanceLevel(Enum):
    OTHER = "OTHER"
    BRONZE = "BRONZE"
    # TODO add more levels here

@dataclass
class Event:
    name: str
    dance_style: DanceStyle
    dance_level: DanceLevel

@dataclass
class Entry:
    """A couple and the event they are competing in"""
    couple: Couple
    event: Event

@dataclass
class PrelimScore:
    entry: Entry
    call_back: bool

@dataclass
class FinalScore:
    entry: Entry
    ranking: int

@dataclass
class ScoreCard:
    judge: Judge
    scores: list[Union[PrelimScore, FinalScore]]

class HeatStatus(Enum):
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    ON_DECK = "ON DECK"
    DANCING = "DANCING"
    FINISHED = "FINISHED"
    SCORED = "SCORED"

@dataclass
class Heat: 
    event: Event # technically this is duplicated data
    heat: str # taking naming suggestions here also should probably convert to enum
    status: HeatStatus
    scores: list[ScoreCard]
    entries: list[Entry]

def batched(items, batch_size: Optional[int] = None):
    """This should be replaced by itertools.batched"""
    if batch_size is None:
        yield items
        return
    if batch_size < 1:
        raise ValueError("Batch Size must be positive")
    i = 0
    while i < len(items):
        yield items[i: i+batch_size] 
        i += batch_size

def generate_heats(entries: list[Entry]) -> list[Heat]:
    """Generate heats of size up to HEAT_SIZE."""
    if len(entries) == 0:
        return []
    event = entries[0].event
    HEAT_SIZE = 10
    for entries_in_heat in batched(entries, HEAT_SIZE):
        yield Heat(event, "foo var", HeatStatus.CREATED, [], entries_in_heat)

def get_call_back_entries(prev_round_scores: list[PrelimScore], call_back_count: Optional[int]) -> list[Entry]:
    """Get the call back entries given the previous round scores"""
    call_backs = Counter([score.entry for score in prev_round_scores if score.call_back]).most_common(call_back_count)
    entries = [call_back[0] for call_back in call_backs]
    yield from generate_heats(entries)

def run():
    couples = get_couples()
    entries = get_entries(couples)


if __name__ == "__main__":
    run()