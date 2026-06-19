from random import Random  # line:1
from collections import Counter  # line:3
from darwin_game.models.player import Action, Player, PlayerNumber, TurnResult  # line:4


class Clippy(Player):  # line:7
    name = "Clippy"  # line:8
    state = None  # line:9

    def make_turn(
        O0OOOO0OO0O0O0O0O,
        O0OOOOO0O000OOO0O: list[TurnResult],
        O0OO00000O00O00O0: PlayerNumber,
        rng: Random,
    ) -> Action:  # line:13
        O00O000O0O00O00O0 = [
            O0O00O00O000000OO.actions[O0OO00000O00O00O0]
            for O0O00O00O000000OO in O0OOOOO0O000OOO0O
        ]  # line:15
        OOOOOO00OOOOO00O0 = [
            O000OOOOOO0O0O0OO.actions[1 - O0OO00000O00O00O0]
            for O000OOOOOO0O0O0OO in O0OOOOO0O000OOO0O
        ]  # line:16
        O0O00000O000O00O0 = len(O0OOOOO0O000OOO0O)  # line:18
        if all(
            [OOO0OOOOOO0000O00 in [0, 2, 3] for OOO0OOOOOO0000O00 in OOOOOO00OOOOO00O0]
        ):  # line:20
            if O0O00000O000O00O0 < 8:  # line:21
                O0OOOO0OO0O0O0O0O.state = "sub8"  # line:22
                return rng.choice([2, 3])  # line:23
            if O0O00000O000O00O0 == 8:  # line:25
                O0OOOO0OO0O0O0O0O.state = "8"  # line:26
                if hash(str(O00O000O0O00O00O0)) > hash(
                    str(OOOOOO00OOOOO00O0)
                ):  # line:27
                    return 3  # line:28
                else:  # line:29
                    return 2  # line:30
            if (
                (O0O00000O000O00O0 > 8)
                and all(
                    [
                        sum(O000O0O0000OOO0O0.actions) in [2, 3, 5]
                        for O000O0O0000OOO0O0 in O0OOOOO0O000OOO0O[8:]
                    ]
                )
                and all(
                    [
                        OO00O000OO00OO0OO in set(OOOOOO00OOOOO00O0)
                        for OO00O000OO00OO0OO in [2, 3]
                    ]
                )
            ):  # line:35
                O0OOOO0OO0O0O0O0O.state = "post8"  # line:36
                if hash("clippy" + str(O0O00000O000O00O0)) % 2 == 0:  # line:37
                    if (O00O000O0O00O00O0[-1] == 3) or (
                        OOOOOO00OOOOO00O0[-1] == 2
                    ):  # line:38
                        return 3  # line:39
                    else:  # line:40
                        return 2  # line:41
                else:  # line:42
                    if (O00O000O0O00O00O0[-1] == 2) or (
                        OOOOOO00OOOOO00O0[-1] == 3
                    ):  # line:43
                        return 3  # line:44
                    else:  # line:45
                        return 2  # line:46
        O0OOOO0OO0O0O0O0O.state = "something_else"  # line:47
        if O00O000O0O00O00O0[:-1] == OOOOOO00OOOOO00O0[1:]:  # line:49
            O0OOOO0OO0O0O0O0O.state = "always_mirror"  # line:50
            if O00O000O0O00O00O0[-1] == 3:  # line:51
                return 5  # line:52
            if O00O000O0O00O00O0[-1] == 5:  # line:53
                return 1  # line:54
            if O00O000O0O00O00O0[-1] == 1:  # line:55
                return 0  # line:56
            if O00O000O0O00O00O0[-1] == 0:  # line:57
                return 5  # line:58
        if len(set(OOOOOO00OOOOO00O0)) == 1:  # line:60
            O0OOOO0OO0O0O0O0O.state = "always_same"  # line:61
            if OOOOOO00OOOOO00O0[-1] < 3:  # line:62
                return 5 - OOOOOO00OOOOO00O0[-1]  # line:63
            else:  # line:64
                return 3  # line:65
        O0O000OOO00OO0O0O = Counter(OOOOOO00OOOOO00O0[-10:])  # line:67
        OOOO0O0OOOO000OOO = 10  # line:68
        OO0000OO0OO0000O0 = {
            O00OO000OO0O0OO0O: O0O000OOO00OO0O0O.get(O00OO000OO0O0OO0O, 0)
            for O00OO000OO0O0OO0O in range(6)
        }  # line:70
        O00000OO0000OO00O = {
            OOO0OO00O0OO00OO0: O0000O00O0000O0O0 / OOOO0O0OOOO000OOO
            for OOO0OO00O0OO00OO0, O0000O00O0000O0O0 in OO0000OO0OO0000O0.items()
        }  # line:72
        O0O0O0OO0O000O00O, O0000O0OOOOO0O0OO = O0O000OOO00OO0O0O.most_common(1)[
            0
        ]  # line:75
        O0OOO0OO00OOOO0OO = O0000O0OOOOO0O0OO / OOOO0O0OOOO000OOO  # line:76
        if O0OOO0OO00OOOO0OO > 0.5 and O0O0O0OO0O000O00O < 3:  # line:78
            O0OOOO0OO0O0O0O0O.state = "bully"  # line:79
            return 5 - int(O0O0O0OO0O000O00O)  # line:80
        O000000OO0O00OOO0 = sum(
            [
                OOO0OOO00OO00OOO0
                for O00O000OO0OO00OOO, OOO0OOO00OO00OOO0 in O00000OO0000OO00O.items()
                if O00O000OO0OO00OOO < 3
            ]
        )  # line:82
        O0OOOO0OO0O0O0O0O.state = "halve_sub3"  # line:83
        if rng.random() < (O000000OO0O00OOO0 * 0.5):  # line:84
            return 2  # line:85
        else:  # line:86
            return 3  # line:87
