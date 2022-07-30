class APIException(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.context = {}
        if code:
            self.context['errorCode'] = code