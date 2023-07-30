"""
重构前留档

Regicide 弑君者
目前还不适用于刚啵元宇宙气象研究院网络对战平台
目前只支持单人模式

由于平台限制只能提交单一文件
所以……
"""

import os
import sys
from collections import deque
from enum import Enum
from inspect import cleandoc
from random import shuffle
from typing import Iterator, Self


class ParseError(BaseException):
    ...


class PokeColor(Enum):
    Red = 0
    Black = 1

    def as_int(self) -> int:
        return self.value


class PokeSuit(Enum):
    Spade = 1  # 黑桃 ♠
    Heart = 2  # 红桃 ♥
    Club = 3  # 梅花 ♣
    Diamond = 4  # 方块 ♦

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
            # case "Clown": return cls.Clown
            # case "Joker": return cls.Joker
            case _: raise ParseError


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
        return self.Suit.as_int() == other.Suit.as_int() and self.Point.as_int == other.Point.as_int


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

    def push_back(self, card: UserCard):
        self.__inner.append(card)

    def push_front(self, card: UserCard):
        self.__inner.appendleft(card)

    def take_back_n_from(self, n: int, discard_pile: Self):
        discard_pile.shuffle()
        cnt = min(n, len(discard_pile))
        for _ in range(cnt):
            self.push_back(discard_pile.pop_back())


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
            return len(self.card_list) == 2 and not is_same
        else:
            return is_same and sum <= 10

    def merge(self) -> MergedCard:
        return MergedCard(self.card_list)

    def count_point(self) -> int:
        return sum(map(lambda card: card.Point.as_int, self.card_list))


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

    def take_n_from(self, n: int, limit:int, card_pile: CardPile):
        cnt = min(limit - self.left(),min(n, len(card_pile)))
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


if sys.platform == "win32":
    def clear_screen():
        os.system("cls")
else:
    def clear_screen():
        os.system("clear")


def hello():
    clear_screen()
    txt = [
        "Regicide——弑君者",
        "命令行Demo版",
        "目前只支持单人模式",
        ""
    ]
    for text in txt:
        print(text)


def CommandLogic():
    while True:
        cmd = input()
        match cmd:
            case "/start": return ChooseLogic()
            case "/rule": return RuleLogic()
            case "/help": return HelpLogic()
            case "/quit": sys.exit(0)
            case _: print("无效指令")


def MenuLogic():
    txt = [
        "/start -> 开始游戏",
        "/rule -> 规则说明",
        "/help -> 寻求帮助",
        "/quit -> 退出游戏"
    ]
    for text in txt:
        print(text)
    CommandLogic()


def RuleLogic():
    txt = [cleandoc("""
    游戏背景：
    一片大陆上有四个王国，但是四个王国的国王、皇后、骑士们都被黑暗的力量给腐蚀了，于是王国的勇士们挺身而出，打倒被黑暗力量侵蚀的国王，将他们唤醒，恢复大陆的和平。

    胜利条件：
    打败四个花色的JQK，共计12个boss。
    """),
           cleandoc("""
    游戏玩法：
    A. 准备牌库
        Boss牌库：将K洗混放在最底下，将Q洗混放在上面，最后将J洗混放在最上面。
            翻开第一张J，这就是当前要打的boss。
            打败boss之后将其丢入弃牌库，翻开下一张boss
        Boss说明：
            J  攻击10   生命20
            Q 攻击15   生命30
            K 攻击20   生命40
        玩家牌库：其余40张牌，开始时获得8张手牌。
    """),
           cleandoc("""
    B. 开始游戏：
        每回合有四个阶段：
            1. 打出卡牌
            2. 激活技能
            3. 对敌人造成伤害
            4. 承受敌人伤害
            
        打出卡牌，关注数字+花色。
        激活技能是根据卡牌花色来的
            ♥红桃治疗：从弃牌堆回卡组底。可以把弃牌堆（已经出过的牌）里的牌返回卡组底部，返回张数就是打出卡牌的数字。
            ♦方片抽牌：从卡组的上方抽牌。玩家轮流补牌，直到抽取了打出卡牌数字的张数。手牌达到上限的人不参与这个抽牌，下家继续抽。
            ♣草花攻击：造成双倍攻击伤害
            ♠黑桃防御：减少敌人等量攻击。打出之后，留在场上的黑桃会持续性减少当前boss的攻击力。
        """),
           cleandoc("""
        对敌人造成实际伤害。（boss能对自己花色的技能免疫）计算实际伤害，此时有三种情况：
            boss的血量<0，就战胜了boss，把它放到弃牌堆，开始新的一轮。
            boss血量=0，那就是感化了这个boss，可以将boss放入牌库里，抽到之后与你并肩作战。
            boss血量>0，他会对你进行一次反击，进入承受伤害阶段

        承受敌人伤害
            你必须从手牌里弃掉任意张卡牌，这些数字合计必须>=计算后的Boss攻击力。
            如果全部手牌加起来的点数<=攻击力，游戏结束。
            如果存在部分手牌加起来的点数>攻击力，那就弃掉这部分手牌进行下一回合。
    """),
           cleandoc("""
    C. 补充出牌方式：

        I: 每个花色的A被称为 “宠物”，宠物和单张卡牌组合打出。
        数字将视为他们的合计值，在原来的基础上拥有他们所有花色的技能。

        II: 卡牌的数字相同时（只要总和不超过10）可以组合打出，称为“连招”。
        数字将视为他们的合计值,在原来的基础上拥有他们所有花色的技能。
        “宠物”不可以当作“连招”打出。
    """),
           ]

    for text in txt[0:-1]:
        print(text)
        input("按回车继续")
    print(txt[-1])
    ReturnMenuLogic()


def HelpLogic():
    print(cleandoc("""
    天生万物以养人，人无一物可报天。
    杀杀杀杀杀杀杀！不忠之人曰可杀！
    不孝之人曰可杀！不仁之人曰可杀！
    不义之人曰可杀！不礼不智不信人。
    大西王曰杀杀杀！我生不为逐鹿来。
    都门懒筑黄金台， 状元百官都如狗。
    总是刀下觳觫材，传令麾下四王子。
    破城不须封刀匕，山头代天树此碑。
    逆天之人立死跪亦死！
    """))
    clear_screen()

    txt = [
        cleandoc("""
        约定：
        出牌为put
        弃牌为discard
        刷新为refresh
        放弃为giveup
        """),
        cleandoc("""
        花色：
        黑桃♠为 S
        红桃♥为 H
        梅花♣为 C
        方块♦为 D
        """),
        cleandoc("""
        特别地：
        如果点数为 A J Q K则需输入这些字母的大写
        否则为数字，正常输入数字即可
        例如：
            出单张：put S K
            出带宠物：put H 10 D A
            出多张：put S 3 H 3 C 3
            弃多张：discard C 10 D 9
        """),
    ]
    for text in txt[:-1]:
        print(text)
        input("按回车继续")
    print(txt[-1])
    ReturnMenuLogic()


def ReturnMenuLogic():
    input("按回车返回主菜单")
    clear_screen()
    return MenuLogic()


def ChooseLogic():
    while True:
        players_number = input("输入游戏人数以开始：")
        if int(players_number) != 1:
            print("目前只能单打喵")
        else:
            return GameLogic()


def GameLogic():
    user_lib = CardPile.make_user_lib_init()
    discard_lib = CardPile.make_empty_init()
    boss_list = BossList.make_init()
    hand_cards = HandCards.make_init()
    hand_cards.take_n_from(8,8, user_lib)

    refresh_times = 2
    guards = 0
    boss = boss_list.next()

    stage = 0
    is_finish = 0
    while is_finish == 0:
        print("当前Boss：")
        print(boss)
        print("现在，你的手牌：")
        print(hand_cards)
        print("出牌吧，骚年！")
        while stage == 0:
            stage = 1

            if hand_cards.count() == 0 and (refresh_times == 0 or len(user_lib) == 0):
                is_finish = -1
                break

            user_input = input().strip()
            uop = UserOperate(user_input)
            match uop.kind:
                case OpKind.Put:
                    if not hand_cards.is_contains_all(uop.card_list):
                        stage = 0
                        print("你可能出了你没有的牌，请重新输入")
                        continue

                    if not uop.put_check():
                        stage = 0
                        print("出牌组合不合法，请重新输入")
                        continue

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
                        hand_cards.take_n_from(super_card.point,8, user_lib)

                case OpKind.Refresh:
                    if refresh_times == 0:
                        stage = 0
                        print("没有刷新次数了，请重新输入")
                        continue

                    hand_cards.discard_all_to(discard_lib)
                    hand_cards.take_n_from(8,8,user_lib)

                case OpKind.GiveUp:
                    stage = 0
                    is_finish = -1
                    break

                case _:
                    stage = 0
                    print("解析失败，请重新输入")

        if is_finish != 0:
            break

        # 出牌结算完成，开始判定Boss状态

        if boss.is_alive():
            # 执行弃牌操作
            # 先判定手里所有牌的点数和是否大于等于boss血量，否则
            # 结束游戏，is_finish = -1
            discard_cnt = max(0, boss.AG - guards)
            if discard_cnt == 0:
                print("你不用弃牌")
                stage = 0

            print("boss状态：")
            print(boss)
            print("现在，你的手牌：")
            print(hand_cards)
            print(f"你需要弃牌至少 {discard_cnt} 点")
            while stage == 1:
                stage = 0

                if hand_cards.count() <= discard_cnt and (refresh_times == 0 or len(user_lib) == 0):
                    is_finish = -1
                    break

                user_input = input().strip()
                uop = UserOperate(user_input)

                match uop.kind:
                    case OpKind.Discard:
                        if not hand_cards.is_contains_all(uop.card_list):
                            stage = 1
                            print("你可能弃了你没有的牌，请重新输入")
                            continue
                        
                        if uop.count_point() < discard_cnt:
                            stage = 1
                            print("弃牌点数不足，请重新输入")
                            continue
                        
                        hand_cards.discard_to(discard_lib, uop.card_list)

                    case OpKind.Refresh:
                        if refresh_times == 0:
                            stage = 1
                            print("没有刷新次数了，请重新输入")
                            continue
                        
                        hand_cards.discard_all_to(discard_lib)
                        hand_cards.take_n_from(8,8, user_lib)
                    case OpKind.GiveUp:
                        is_finish = -1
                        break

                    case _:
                        stage = 1
                        print("解析失败，请重新输入")
        else:
            stage = 0
            guards = 0
            if boss.can_convert():
                hand_cards.add_card(boss.convert())
                print(f"你感化了Boss，获得{boss.convert()}")
            else:
                print(f"你击败了{boss.settlement_show()}")

            if len(boss_list) == 0:
                is_finish = 1
            else:
                boss = boss_list.next()

    if is_finish == 1:
        print("你赢了")
    else:
        print("你输了")

    ReturnMenuLogic()

def main():
    hello()
    MenuLogic()


main()
