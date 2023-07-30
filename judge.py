"""
Regicide 弑君者
适用于刚啵元宇宙气象研究院网络对战平台
目前只支持单人模式

由于平台限制只能提交单一文件
所以……
"""

import json

from inspect import cleandoc

from collections import deque
from random import shuffle

from enum import Enum
from typing import Iterator, Self


class ParseError(BaseException):
    ...


class PokeColor(Enum):
    Red = 0
    Black = 1

    def as_int(self) -> int:
        return self.value


class PokeSuit(Enum):
    Spade = 1  # 黑桃
    Heart = 2  # 红桃
    Club = 3  # 梅花
    Diamond = 4  # 方块

    """
    单人模式目前还没用，多人模式还没开发出来
    所以临时占位罢了
    """
    Joker = 0  # 王牌
    # Clown = 9  # 还是王牌

    def as_int(self) -> int:
        return self.value

    def color(self) -> PokeColor:
        return PokeColor(self.value % 2)

    def __repr__(self) -> str:
        match self.value:
            case 1: return "S"
            case 2: return "H"
            case 3: return "C"
            case 4: return "D"
            case _: return "*"

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def parse_from_str(cls, ssuit: str):
        match ssuit:
            case "S": return cls.Spade
            case "H": return cls.Heart
            case "C": return cls.Club
            case "D": return cls.Diamond
            # case "Clown": return cls.Clown
            # case "Joker": return cls.Joker
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
            case p:
                p = int(p)
                assert (1 < p and p <= 10)
                return cls(p)

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

    大小王还没做，别急
    """
    __slots__ = ["Suit", "Point"]

    def __init__(self, suit: PokeSuit, point: PokePoint) -> None:
        self.Suit = suit
        self.Point = point

    @classmethod
    def parse_from_str_pair(cls, ssuit: str, spoint: str):
        return cls(PokeSuit.parse_from_str(ssuit), PokePoint.parse_from_str(spoint))

    def __eq__(self, other: Self) -> bool:
        return (self.Suit.as_int() == other.Suit.as_int()
                and self.Point.as_int == other.Point.as_int)


class UserCard(PokeCard):
    """
    用户可以使用的牌，携带特殊效果
    """

    def __init__(self, card: PokeCard) -> None:
        super().__init__(card.Suit, card.Point)

    def is_pet(self) -> bool:
        return self.Point.as_int == 1

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

    def __repr__(self) -> str:
        return f"Boss{{{self.Suit}, AG: {self.AG}, HP: {self.HP}}}"

    def __str__(self) -> str:
        return repr(self)

    def show(self) -> str:
        return f"Boss {self.Suit.show()} {self.AG} {self.HP}"


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
    def make_user_lib_init(cls):
        ls = [UserCard(PokeCard(PokeSuit(suit + 1), PokePoint(point + 1)))
              for suit in range(0, 4) for point in range(0, 10)]
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

    def push(self, card: UserCard):
        self.__inner.append(card)

    def take_back_n_from(self, n: int, discard_pile: Self):
        discard_pile.shuffle()
        cnt = min(n, len(discard_pile))
        for _ in range(cnt):
            self.push(discard_pile.pop_back())


class OpKind(Enum):
    Invalid = 0
    Put = 1
    Discard = 2
    Refresh = 3
    GiveUp = 4

    @classmethod
    def parse_from(cls, s: str):
        match s:
            case "put": return cls.Put
            case "discard": return cls.Discard
            case "refresh": return cls.Refresh
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
            case OpKind.Invalid: self.card_list = []
            case OpKind.Refresh | OpKind.GiveUp:
                try:
                    _ = next(siter)
                except:
                    return
                else:
                    self.kind = OpKind.Invalid
            case _:
                try:
                    self.card_list = card_list_from_iter(siter)
                    assert (len(self.card_list) != 0)
                except:
                    self.kind = OpKind.Invalid
                else:
                    return

    def put_check(self) -> bool:
        assert (self.kind == OpKind.Put)
        if len(self.card_list) == 1:
            return True
        
        has_pet = False
        is_same = True

        fstp = self.card_list[0].Point.as_int
        sum = fstp
        for card in self.card_list:
            has_pet = has_pet or card.is_pet()
            is_same = is_same and (card.Point.as_int == fstp)
            sum += card.Point.as_int
        if has_pet:
            return (len(self.card_list) == 2) and (not is_same)
        else:
            return is_same and (sum <= 10)

    def merge(self) -> MergedCard:
        return MergedCard(self.card_list)

    def count_point(self) -> int:
        return sum(map(lambda card: card.Point.as_int, self.card_list),0)


class HandCards:
    __slots__ = ["has"]

    def __repr__(self) -> str:
        return repr(list(self.has))

    def __str__(self) -> str:
        return repr(self)

    def __init__(self, sets: list[UserCard]) -> None:
        self.has = sets

    def add_card(self, card: UserCard):
        if not (card in self.has):
            self.has.append(card)

    def take_n_from(self, n: int, card_pile: CardPile):
        cnt = min(n, len(card_pile))
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
            discard_pile.push(self.has.pop())

    def discard_to(self, discard_pile: CardPile, cards: list[UserCard]):
        for card in cards:
            self.has.remove(card)
            discard_pile.push(card)

    def show(self) -> str:
        result = ""
        for card in self.has:
            result += f"{card.show()} "
        return result.strip()


def sendmsg(jsonmsg):
    print(json.dumps(jsonmsg))


def send_failure(msg: str):
    jsonmsg = {
        "command": "finish",
        "content": {
            "0": -1,
            "1": 0
        },
        "display": msg
    }
    sendmsg(jsonmsg)

def send_success(msg: str):
    jsonmsg = {
        "command": "finish",
        "content": {
            "0": 1,
            "1": 0
        },
        "display": msg
    }
    sendmsg(jsonmsg)

def GameLogic():
    # 忽略第一行
    input()
    
    # 忽略玩家2
    

    out_content = {
        "command": "request",
        "content": {
            "0": "",
        },
        "display": ""
    }

    # 直接赢了

    user_lib = CardPile.make_user_lib_init()
    discard_lib = CardPile.make_empty_init()
    boss_list = BossList.make_init()
    hand_cards = HandCards.make_init()
    hand_cards.take_n_from(8, user_lib)
    refresh_times = 2
    guards = 0
    boss = boss_list.next()


    # 胜利者测试
    is_finish = 0

    # 先忽略玩家2
    # sendmsg({
    #     "command": "request",
    #     "content": {
    #         "1": cleandoc(f"""
    #         {boss.show()}
    #         {hand_cards.show()}
    #         put
    #         """),
    #     },
    #     "display": "Ignore 2"
    # })
    # input()

    while is_finish == 0:

        if hand_cards.count() == 0 and (refresh_times == 0 or len(user_lib) == 0):
            is_finish = -1
            break

        out_content["content"]["0"] = cleandoc(f"""
        {boss.show()}
        {hand_cards.show()}
        put
        """)

        out_content["display"] = cleandoc(f"""
        Current Boss: {boss}
        The cards in your hand: {hand_cards}
        So brace yourselves for assault!
        """)

        sendmsg(out_content)

        in_content = json.loads(input()) 
        if in_content["0"]["verdict"] != "OK":
            send_failure("Unknown Error")
            return

        user_input = in_content["0"]["raw"]
        uop = UserOperate(user_input)
        match uop.kind:
            case OpKind.Put:
                if not hand_cards.is_contains_all(uop.card_list):
                    send_failure("Nonexistent Cards")
                    return

                if not uop.put_check():
                    send_failure("Illegal Combination")
                    return

                # 执行出牌
                hand_cards.discard_to(discard_lib, uop.card_list)

                super_card = uop.merge()
                super_card.disable(boss.Suit)
                if super_card.is_empty():
                    pass

                boss.suffer(super_card.point)
                if super_card.has_spade():
                    guards += super_card.point
                if super_card.has_heart():
                    user_lib.take_back_n_from(
                        super_card.point, discard_lib)
                if super_card.has_club():
                    boss.suffer(super_card.point)
                if super_card.has_diamond():
                    hand_cards.take_n_from(super_card.point, user_lib)

            case OpKind.Refresh:
                if refresh_times == 0:
                    send_failure("No Remaining Refresh Times")
                    return

                hand_cards.discard_all_to(discard_lib)
                hand_cards.take_n_from(8, user_lib)

            case OpKind.GiveUp:
                send_failure("Never Gonna Give You Up")
                return

            case _:
                send_failure("Parse Error")
                return

        if is_finish != 0:
            break

        # 出牌结算完成，开始判定Boss状态

        if boss.is_alive():
            # 执行弃牌操作
            # 先判定手里所有牌的点数和是否大于等于boss血量，否则
            # 结束游戏，is_finish = -1
            discard_cnt = max(boss.AG - guards,0)
            if discard_cnt == 0:
                # 不用弃牌
                continue

            if hand_cards.count() <= discard_cnt and (refresh_times == 0 or len(user_lib) == 0):
                is_finish = -1
                break
            
            # 存在继续游戏的可能

            out_content["content"]["0"] = cleandoc(f"""
            {boss.show()}
            {hand_cards.show()}
            discard {discard_cnt}
            """)

            out_content["display"] = cleandoc(f"""
            Current Boss: {boss}
            The cards in your hand: {hand_cards}
            You need to discard at least {discard_cnt} points.
            """)
            sendmsg(out_content)

            in_content = json.loads(input()) 
            if in_content["0"]["verdict"] != "OK":
                send_failure("Unknown Error")
                return

            user_input = in_content["0"]["raw"]
            uop = UserOperate(user_input)

            match uop.kind:
                case OpKind.Discard:
                    if not hand_cards.is_contains_all(uop.card_list):
                        send_failure("Nonexistent Cards")
                        return
                    
                    if uop.count_point() < discard_cnt:
                        send_failure("Points Not Enough")
                        return
                    
                    hand_cards.discard_to(discard_lib, uop.card_list)

                case OpKind.Refresh:
                    if refresh_times == 0:
                        send_failure( "No Remaining Refresh Times")
                        return

                    hand_cards.discard_all_to(discard_lib)
                    hand_cards.take_n_from(8, user_lib)

                case OpKind.GiveUp:
                    send_failure( "Never Gonna Give You Up")
                    return

                case _:
                    send_failure( "Parse Error")
                    return

        else:
            guards = 0
            if boss.can_convert():
                hand_cards.add_card(boss.convert())
            if len(boss_list) == 0:
                is_finish = 1
            else:
                boss = boss_list.next()

    if is_finish == 1:
        send_success("Everything is born to nourish people, and no one has anything to repay the heavens! You killed all of them!")
    else:
        send_failure("Congratulations! you lost your game following the normal playing process.")

GameLogic()
