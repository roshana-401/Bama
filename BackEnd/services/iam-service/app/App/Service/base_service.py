from ..core.config import setting


class BaseService:
    def __init__(self, config = setting) :
        self.config = config

