import sys
import os
from stdpile import HandCards, CardPile, BossList
from userop import UserOperate, OpKind
from game_txt import hello_txt, menu_txt, rule_txt, kill_txt, help_txt
if sys.platform == "win32":
    def clear_screen():
        os.system("cls")
else:
    def clear_screen():
        os.system("clear")


def hello():
    clear_screen()
    txt = hello_txt
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
    txt = menu_txt
    for text in txt:
        print(text)
    CommandLogic()


def RuleLogic():
    txt = rule_txt

    for text in txt[0:-1]:
        print(text)
        input("按回车继续")
    print(txt[-1])
    ReturnMenuLogic()


def HelpLogic():
    print(kill_txt)
    clear_screen()

    txt = help_txt
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

                case OpKind.Pass:
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

                case OpKind.Invalid:
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
                    case OpKind.Put:
                        if not hand_cards.is_contains_all(uop.card_list):
                            stage = 1
                            print("你可能弃了你没有的牌，请重新输入")
                            continue

                        if uop.count_point() < discard_cnt:
                            stage = 1
                            print("弃牌点数不足，请重新输入")
                            continue

                        hand_cards.discard_to(discard_lib, uop.card_list)

                    case OpKind.Pass:
                        if refresh_times == 0:
                            stage = 1
                            print("没有刷新次数了，请重新输入")
                            continue

                        hand_cards.discard_all_to(discard_lib)
                        hand_cards.take_n_from(8, 8, user_lib)
                    case OpKind.GiveUp:
                        is_finish = -1
                        break

                    case OpKind.Invalid:
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
