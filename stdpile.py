from typing import Self
from random import shuffle
from stdcard import BossCard, UserCard, PokeCard, PokeSuit, PokePoint
from collections import deque


class BossList:
    __slots__ = ["__inner"]

    def __init__(self, cards: list[BossCard]) -> None:
        self.__inner = cards

    @classmethod
    def make_init(cls):
        ls = []
        for p in range(2, -1, -1):
            curr = [BossCard(PokeCard(PokeSuit(suit + 1), PokePoint(15 + p * 5)))
                    for suit in range(0, 4)]
            shuffle(curr)
            ls += curr
        return cls(ls)

    def __len__(self) -> int:
        return len(self.__inner)

    def next(self) -> BossCard:
        return self.__inner.pop()


class CardPile:
    __slots__ = ["__inner"]

    def __repr__(self) -> str:
        return repr(list(self.__inner))

    def str(self) -> str:
        return repr(self)

    def __init__(self, cards: list[UserCard]) -> None:
        self.__inner = deque(cards)

    @classmethod
    def make_user_lib_init(cls,jokers :int):
        ls = [UserCard(PokeCard(PokeSuit(suit + 1), PokePoint(point + 1)))
              for suit in range(0, 4) for point in range(0, 10)]
        for _ in range(jokers):
            ls.append(UserCard.make_joker())
        shuffle(ls)
        return cls(ls)

    @classmethod
    def make_empty_init(cls):
        return cls([])

    def shuffle(self):
        shuffle(self.__inner)

    def __len__(self) -> int:
        return len(self.__inner)

    def pop_back(self) -> UserCard:
        return self.__inner.pop()

    def pop_front(self) -> UserCard:
        return self.__inner.popleft()

    def push_back(self, card: UserCard):
        self.__inner.append(card)

    def push_front(self, card: UserCard):
        self.__inner.appendleft(card)

    def take_back_n_from(self, n: int, discard_pile: Self):
        discard_pile.shuffle()
        cnt = min(n, len(discard_pile))
        for _ in range(cnt):
            self.push_back(discard_pile.pop_back())

    


class HandCards:
    __slots__ = ["has"]

    def __repr__(self) -> str:
        return repr(list(self.has))

    def str(self) -> str:
        return repr(self)

    def __init__(self, sets: list[UserCard]) -> None:
        self.has = sets

    def add_card(self, card: UserCard):
        if not (card in self.has):
            self.has.append(card)

    def take_n_from(self, n: int, limit: int, card_pile: CardPile):
        cnt = min(limit - self.left(), min(n, len(card_pile)))
        for _ in range(cnt):
            self.add_card(card_pile.pop_front())

    def count(self) -> int:
        sum = 0
        for x in self.has:
            sum += x.Point.as_int
        return sum

    def left(self) -> int:
        return len(self.has)

    def is_contains_all(self, cards: list[UserCard]) -> bool:
        is_ok = True
        for card in cards:
            is_ok = is_ok and (card in self.has)
        return is_ok

    @classmethod
    def make_init(cls):
        return cls([])

    def discard_all_to(self, discard_pile: CardPile):
        cnt = self.left()
        for _ in range(cnt):
            discard_pile.push_back(self.has.pop())

    def discard_to(self, discard_pile: CardPile, cards: list[UserCard]):
        for card in cards:
            self.has.remove(card)
            discard_pile.push_back(card)

