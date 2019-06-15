from .base import BaseFilter
from ..factory import RequestFactory


class RequestFilter(BaseFilter):
    base_factory = RequestFactory

    def _get_data(self):
        return self.factory.reqs