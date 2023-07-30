from enum import Enum

class UserMode:
    __slots__ = ["players"]
    def __init__(self,num:int) -> None:
        self.players = num

import stdcard,stdpile

class UserState():
    __slots__ = ["id","hand_cards","is_alive","card_mark"]
    
