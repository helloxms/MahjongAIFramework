class MJConstants:
    class Action:
        READY = 0
        START = 1
        TAKE = 2
        CHOW = 3
        PONG = 4
        KONG = 5
        PLAY = 6
        TIN = 7
        HU = 8
        PASS = 9

    class round_act_state:
        START = 0
        CHECK_TAKE = 1
        ACT_TAKE = 2
        CHECK_CHOW = 3
        CALL_CHOW = 4
        ACT_CHOW = 5
        CHECK_PONG = 6
        CALL_PONG = 7
        ACT_PONG = 8
        CHECK_KONG = 9
        CALL_KONG = 10
        ACT_KONG = 11
        CHECK_TIN = 12
        CALL_TIN = 13
        ACT_TIN = 14
        CHECK_PLAY = 15
        ACT_PLAY = 16
        CHECK_HU = 17
        CALL_HU = 18
        ACT_HU = 19
        FINISHED = 20

    ACT_ID_STR_MAP = {
        0: 'ready', 1: 'start', 2: 'take', 3: 'chow', 4: 'pong', 5: 'kong', 6: 'play',
        7: 'tin', 8: 'hu', 9: 'pass'

    }

    ACT_STR_ID_MAP = {
        'ready': 0, 'start': 1, 'take': 2, 'chow': 3, 'pong': 4, 'kong': 5, 'play': 6,
        'tin': 7, 'hu': 8, 'pass': 9
    }
