# Comp Manager Orchestrator
from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from typing import Generic, Optional, Union
from dataclasses import dataclass
from enum import Enum

@dataclass
class Judge:
    """A judge"""
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
    prelim_scores: list[PrelimScore]
    final_scores: list[FinalScore]

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
    status: HeatStatus
    scores: list[ScoreCard]
    entries: list[Entry]

@dataclass
class Round: # TODO rename this to something better, `round` is a reserved keyword
    event: Event
    bracket: Bracket # lol help I can't just call this round again can I?
    heats: list[Heat]

class Bracket(Enum):
    R_16 = 16 # okay I feel like this won't actually happen in real life, what do we do if we have more competitors than quarterfinals? should we have an "overflow" bracket?
    QUARTER = 4
    SEMI = 2
    FINAL = 1

    @staticmethod
    def get_next_bracket(current_bracket: Bracket) -> Optional[Bracket]:
        if current_bracket == Bracket.R_16:
            return Bracket.QUARTER
        elif current_bracket == Bracket.QUARTER:
            return Bracket.SEMI
        elif current_bracket == Bracket.SEMI:
            return Bracket.FINAL
        elif current_bracket == Bracket.FINAL:
            return None
        else:
            raise ValueError("Invalid Bracket")

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
    
DEFAULT_HEAT_SIZE = 10

def generate_heats(entries: list[Entry], heat_size = DEFAULT_HEAT_SIZE) -> list[Heat]:
    """Generate heats of size up to heat_size.
    
    TODO we should probably consider generating based off number of heats as well.
    """
    if len(entries) == 0:
        return []
    event = entries[0].event
    for entries_in_heat in batched(entries, heat_size):
        yield Heat(event, HeatStatus.CREATED, [], entries_in_heat)

def get_call_back_heats(prev_round_scores: list[PrelimScore], num_heats: int, heat_size = DEFAULT_HEAT_SIZE) -> list[Heat]:
    """Get the call back entries given the previous round scores"""
    call_back_count = num_heats * heat_size
    call_backs = Counter([score.entry for score in prev_round_scores if score.call_back]).most_common(call_back_count)
    entries = [call_back[0] for call_back in call_backs]
    yield from generate_heats(entries)

def score_final(final_scores: list[FinalScore]):
    pass

def get_next_round(current_round: Round) -> Round:
    next_bracket = Bracket.get_next_bracket(current_round.bracket)
    if next_bracket is None:
        raise ValueError("No next round")
    scores = []
    for heat in current_round.heats:
        for score_card in heat.scores:
            scores.extend(score_card.prelim_scores)

    # TODO we might not actually want to create a new round here, we might instead want to pregenerate all the rounds and then just update the heats.
    return Round(current_round.event, next_bracket, get_call_back_heats(scores, next_bracket.value))

def generate_initial_round(entries: list[Entry]) -> Round:
    heats = generate_heats(entries)
    return Round(entries[0].event, Bracket.R_16, heats)

def get_couples():
    return []

def get_entries_by_event(couples: list[Couple]) -> dict[Event, list[Entry]]:
    return {}

def generate_schedule(entries_by_event: dict[Event, list[Entry]]) -> list[Heat]:
    return []

def update_competitors(couples: list[Couple]) -> list[Couple]:
    return []

def finalize_heat(heat: Heat) -> Heat:
    """Do actual comp and judging"""
    return heat

def queue_heat(heat: Heat) -> Heat:
    """Do floor captain routine"""
    return heat

def score_heat(heat: Heat) -> None:
    return None

def check_round_finished(heat: Heat) -> bool:
    return True

def run():
    # Run Registration
    couples = get_couples()
    entries_by_event = get_entries_by_event(couples)
    # Generate Preliminary schedule a few weeks out
    schedule = generate_schedule(entries_by_event)
    # Day of comp registration changes
    couples = update_competitors(couples)
    entries_by_event = get_entries_by_event(couples)

    # do the following in parallel

    # On the Floor
    for heat in schedule:
        heat = finalize_heat(heat)
        # run the heat

    # On Deck
    for heat in schedule:
        heat = queue_heat(heat)
        # run the heat

    # Generate next round
    for heat in schedule:
        score_heat(heat)
        if check_round_finished(heat):
            round = get_next_round(round)

    for event, entries in entries_by_event.items():
        round = generate_initial_round(entries)

if __name__ == "__main__":
    run()