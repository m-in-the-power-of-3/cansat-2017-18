class UAVTalkError(Exception):
    def __init__(self, str):
        super(Exception, self).__init__(str)


class RevolutionError(Exception):
    def __init__(self, str):
        super(Exception, self).__init__(str)


class TSL2561Error(Exception):
    def __init__(self, str):
        super(Exception, self).__init__(str)


class ADS1115Error(Exception):
    def __init__(self, str):
        super(Exception, self).__init__(str)


class FuseError(Exception):
    def __init__(self, str):
        super(Exception, self).__init__(str)

