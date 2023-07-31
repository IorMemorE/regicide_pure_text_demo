
class UserMode:
    __slots__ = ["players","jokers","limit"]

    def __init__(self, num: int) -> None:
        self.players = num
        self.jokers = max(0,num - 2)
        self.limit = 9 - num


class UserState():
    __slots__ = ["id", "hand_cards", "is_alive", "card_mark"]
