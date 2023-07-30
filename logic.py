import sys
import os
from inspect import cleandoc
from stdpile import HandCards, CardPile, BossList
from userop import UserOperate, OpKind

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
    user_lib = CardPile.make_user_lib_init(0)
    discard_lib = CardPile.make_empty_init()
    boss_list = BossList.make_init()
    hand_cards = HandCards.make_init()
    hand_cards.take_n_from(8, 8, user_lib)

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
                        hand_cards.take_n_from(super_card.point, 8, user_lib)

                case OpKind.Refresh:
                    if refresh_times == 0:
                        stage = 0
                        print("没有刷新次数了，请重新输入")
                        continue

                    hand_cards.discard_all_to(discard_lib)
                    hand_cards.take_n_from(8, 8, user_lib)

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
                        hand_cards.take_n_from(8, 8, user_lib)
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
