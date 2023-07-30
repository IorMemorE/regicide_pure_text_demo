from enum import Enum 
from parse_error import ParseError
from typing import Self

class PokeSuit(Enum):
    Spade = 1  # 黑桃 ♠
    Heart = 2  # 红桃 ♥
    Club = 3  # 梅花 ♣
    Diamond = 4  # 方块 ♦

    Joker = -1  # 大王

    def as_int(self) -> int:
        return self.value
    def __eq__(self, other: Self) -> bool:
        return self.as_int() == other.as_int()

    def __repr__(self) -> str:
        match self.value:
            case 1: return "♠"
            case 2: return "♥"
            case 3: return "♣"
            case 4: return "♦"
            case _: return "🃏"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def parse_from_str(cls, ssuit: str):
        match ssuit:
            case "S": return cls.Spade
            case "H": return cls.Heart
            case "C": return cls.Club
            case "D": return cls.Diamond
            case "*": return cls.Joker
            case _: raise ParseError

    def show(self) -> str:
        match self.value:
            case 1: return "S"
            case 2: return "H"
            case 3: return "C"
            case 4: return "D"
            case _: return "*"


class PokePoint:
    __slots__ = ["as_int"]

    def __init__(self, point: int) -> None:
        self.as_int = point

    def __repr__(self) -> str:
        match self.as_int:
            case 0: return "*"
            case 1: return "A"
            case 15: return "J"
            case 20: return "Q"
            case 25: return "K"
            case p:
                assert (1 < p and p <= 10)
                return f"{p}"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def parse_from_str(cls, spoint: str):
        match spoint:
            case "J": return cls(15)
            case "Q": return cls(20)
            case "K": return cls(25)
            case "A": return cls(1)
            case "*": return cls(0)
            case p:
                p = int(p)
                assert (1 < p and p <= 10)
                return cls(p)
    
    def __eq__(self, other: Self) -> bool:
        return self.as_int == other.as_int

    def show(self) -> str:
        return repr(self)


class PokeCard:
    """
    扑克基类
    每张扑克都有花色和点数

    特别的，有以下点数
    j -> 15
    q -> 20
    k -> 25
    """
    __slots__ = ["Suit", "Point"]

    def __init__(self, suit: PokeSuit, point: PokePoint) -> None:
        self.Suit = suit
        self.Point = point

    @classmethod
    def parse_from_str_pair(cls, ssuit: str, spoint: str):
        return cls(PokeSuit.parse_from_str(ssuit), PokePoint.parse_from_str(spoint))

    def __eq__(self, other: Self) -> bool:
        return self.Suit == other.Suit and self.Point == other.Point


class UserCard(PokeCard):
    """
    用户可以使用的牌，携带特殊效果
    """

    def __init__(self, card: PokeCard) -> None:
        super().__init__(card.Suit, card.Point)

    def is_pet(self) -> bool:
        return self.Point.as_int == 1
    
    def is_joker(self) -> bool:
        return self.Suit == PokeSuit.Joker
    

    @classmethod
    def make_joker(cls):
        return cls(PokeCard(PokeSuit.Joker,PokePoint(0))) 

    def __repr__(self) -> str:
        return f"Card{{{self.Suit} {self.Point}}}"

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: Self) -> bool:
        return super().__eq__(other)
    
    def show(self) -> str:
        return f"{self.Suit.show()} {self.Point.show()}"


class BossCard(PokeCard):
    __slots__ = ["AG", "HP"]

    def __init__(self, card: PokeCard) -> None:
        assert (card.Point.as_int > 10)
        super().__init__(card.Suit, card.Point)
        self.AG = card.Point.as_int - 5
        self.HP = 2 * self.AG

    def suffer(self, damage: int):
        self.HP -= damage

    def attact(self, guards: int):
        return max(0, self.AG - guards)

    def is_alive(self):
        return self.HP > 0

    def can_convert(self):
        return self.HP == 0

    def convert(self) -> UserCard:
        assert (self.HP == 0)
        return UserCard(super())

    def settlement_show(self) -> str:
        return f"Boss{{{self.Suit} {self.Point}}}"

    def __repr__(self) -> str:
        return f"Boss{{{self.Suit}, AG: {self.AG}, HP: {self.HP}}}"

    def __str__(self) -> str:
        return repr(self)
    
    def show(self) -> str:
        return f"Boss {self.Suit.show()} {self.AG} {self.HP}"