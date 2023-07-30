﻿# Regicide 弑君者

[桌游官网](https://badgersfrommars.com/)

[官方手游](https://play.google.com/store/apps/details?id=com.bfm.regicidecompanion)

## 说明

将来适用于刚啵元宇宙气象研究院网络对战平台

目前只支持单人模式

`main.py`为命令行Demo

`judge.py` 为将来的裁判机版本

由于对战平台限制只能提交单一文件，所以没有写成分库的形式

##  游戏背景

一片大陆上有四个王国，但是四个王国的国王、皇后、骑士们都被黑暗的力量给腐蚀了，于是王国的勇士们挺身而出，打倒被黑暗力量侵蚀的国王，将他们唤醒，恢复大陆的和平。

## 胜利条件

打败四个花色的JQK，共计12个boss。

## 游戏玩法

### A. 准备牌库
1. Boss牌库：
    - 将K洗混放在最底下，将Q洗混放在上面，最后将J洗混放在最上面。
    - 翻开第一张J，这就是当前要打的boss。
    - 打败boss之后将其丢入弃牌库，翻开下一张boss
2. Boss说明：
    - J  攻击10   生命20
    - Q 攻击15   生命30
    - K 攻击20   生命40
3. 玩家牌库：其余40张牌，开始时获得8张手牌。

### B. 开始游戏：
1. 每回合有四个阶段：
    1. 打出卡牌
    2. 激活技能
    3. 对敌人造成伤害
    4. 承受敌人伤害
            
2. 打出卡牌，关注数字+花色。
    1. 激活技能是根据卡牌花色来的
        - ♥红桃治疗：从弃牌堆回卡组底。可以把弃牌堆（已经出过的牌）里的牌返回卡组底部，返回张数就是打出卡牌的数字。
        - ♦方片抽牌：从卡组的上方抽牌。玩家轮流补牌，直到抽取了打出卡牌数字的张数。手牌达到上限的人不参与这个抽牌，下家继续抽。
        - ♣草花攻击：造成双倍攻击伤害
        - ♠黑桃防御：减少敌人等量攻击。打出之后，留在场上的黑桃会持续性减少当前boss的攻击力。
    2. 对敌人造成实际伤害。（boss能对自己花色的技能免疫）计算实际伤害，此时有三种情况：
        - boss的血量<0，就战胜了boss，把它放到弃牌堆，开始新的一轮。
        - boss血量=0，那就是感化了这个boss，可以将boss放入牌库里，抽到之后与你并肩作战。
        - boss血量>0，他会对你进行一次反击，进入承受伤害阶段

    3. 承受敌人伤害
        - 你必须从手牌里弃掉任意张卡牌，这些数字合计必须>=计算后的Boss攻击力。
        - 如果全部手牌加起来的点数<=攻击力，游戏结束。
        - 如果存在部分手牌加起来的点数>攻击力，那就弃掉这部分手牌进行下一回合。

### C. 补充出牌方式：

1. 每个花色的A被称为 “宠物”，宠物和单张卡牌组合打出。数字将视为他们的合计值，在原来的基础上拥有他们所有花色的技能。

2. 卡牌的数字相同时（只要总和不超过10）可以组合打出，称为“连招”。数字将视为他们的合计值,在原来的基础上拥有他们所有花色的技能。

3. “宠物”不可以当作“连招”打出。


### D. 玩家交互
1. 约定：
    - 出牌为`put`
    - 弃牌为`discard`
    - 刷新为`refresh`
    - 放弃为`giveup`

2. 花色：
    - 黑桃♠为 `S`
    - 红桃♥为 `H`
    - 梅花♣为 `C`
    - 方块♦为 `D`

3. 特别地：
    如果点数为 `A` `J` `Q` `K`则需输入这些字母的大写
    否则为数字，正常输入数字即可

4. 例如：
    - 出单张：`put S K`
    - 出带宠物：`put H 10 D A`
    - 出多张：`put S 3 H 3 C 3`
    - 弃多张：`discard C 10 D 9`
