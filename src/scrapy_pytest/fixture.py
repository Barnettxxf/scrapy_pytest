from .utils.response import RetrieveResponse
from .settings import Settings


def format_response_fixture(spidercls, request, settings=Settings):
    storage = RetrieveResponse(settings=settings)
    return storage.retrieve_response(spidercls, request)
