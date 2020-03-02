class MJConstants:

    class Action:
        START  = 0
        TAKE  = 1
        CHOW  = 2
        PONG = 3
        KONG = 4
        PLAY = 5
        TIN = 6
        HU = 7
        
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
        CHECK_TIN  = 12
        CALL_TIN = 13
        ACT_TIN = 14
        CHECK_PLAY =15
        ACT_PLAY = 16
        CHECK_HU = 17
        CALL_HU = 18
        ACT_HU = 19
        FINISHED = 20

