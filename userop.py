from enum import Enum
from parse_error import ParseError
from typing import Iterator
from stdcard import UserCard, PokeCard, PokeSuit


class OpKind(Enum):
    Invalid = 0
    Put = 1
    Pass = 2
    GiveUp = 3

    @classmethod
    def parse_from(cls, s: str):
        match s:
            case "put": return cls.Put
            case "pass": return cls.Pass
            case "giveup": return cls.GiveUp
            case _: return cls.Invalid


def card_list_from_iter(siter: Iterator[str]) -> list[UserCard]:
    plist = list(siter)
    if len(plist) % 2 != 0:
        raise ParseError
    return [UserCard(PokeCard.parse_from_str_pair(plist[2*i].strip(), plist[2*i+1].strip()))
            for i in range(len(plist)//2)]


class MergedCard:
    __slots__ = ["suits", "point"]

    def __init__(self, cards: list[UserCard]) -> None:
        self.suits: set[PokeSuit] = set()
        self.point: int = 0
        for card in cards:
            self.suits.add(card.Suit)
            self.point += card.Point.as_int

    def is_empty(self) -> bool:
        return len(self.suits) == 0

    def disable(self, boss_s_suit: PokeSuit):
        self.suits.discard(boss_s_suit)

    def has_spade(self) -> bool:
        return PokeSuit.Spade in self.suits

    def has_heart(self) -> bool:
        return PokeSuit.Heart in self.suits

    def has_club(self) -> bool:
        return PokeSuit.Club in self.suits

    def has_diamond(self) -> bool:
        return PokeSuit.Diamond in self.suits


class UserOperate:
    __slots__ = ["kind", "card_list"]

    def __init__(self, inp: str) -> None:
        if len(inp) == 0 or len(inp) > 100:
            self.kind = OpKind.Invalid
            return

        siter = iter(inp.split())

        self.kind = OpKind.parse_from(next(siter).strip())
        match self.kind:
            case OpKind.Put:
                try:
                    self.card_list = card_list_from_iter(siter)
                    assert (len(self.card_list) != 0)
                except:
                    self.kind = OpKind.Invalid
                else:
                    return
            case OpKind.Pass | OpKind.GiveUp:
                try:
                    _ = next(siter)
                except:
                    return
                else:
                    self.kind = OpKind.Invalid
            case _:
                self.card_list = []

    def put_check(self) -> bool:
        assert (self.kind == OpKind.Put)
        if len(self.card_list) == 1:
            return True
        has_pet = False
        is_same = True
        fstp = self.card_list[0].Point.as_int
        sum = fstp
        for card in self.card_list:
            if card.is_joker():
                continue
            has_pet = has_pet or card.is_pet()
            is_same = is_same and (card.Point.as_int == fstp)
            sum += card.Point.as_int

        if has_pet:
            return len(self.card_list) == 2 and not is_same
        else:
            return is_same and sum <= 10

    def merge(self) -> MergedCard:
        return MergedCard(self.card_list)

    def count_point(self) -> int:
        return sum(map(lambda card: card.Point.as_int, self.card_list))
