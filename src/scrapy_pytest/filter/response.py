from .base import BaseFilter
from ..factory import ResponseFactory


class ResponseFilter(BaseFilter):
    base_factory = ResponseFactory

    def _get_data(self):
        return self.factory.result
