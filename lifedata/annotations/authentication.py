from typing import Protocol

from loguru import logger

from .annotator import Annotator
from .annotator import AnnotatorRepository
from .annotator import UserInfo


class TokenDecoder(Protocol):
    def decode(self, token: str) -> UserInfo:
        ...


class AuthenticationService:
    def __init__(
        self, annotator_repository: AnnotatorRepository, token_decoder: TokenDecoder
    ):
        self._repository = annotator_repository
        self._token_decoder = token_decoder

    def authenticate(self, token: str) -> Annotator:
        try:
            info = self._token_decoder.decode(token)
        except Exception as exc:
            logger.exception(f"Cannot decode token: {exc}")
            raise
        return self._repository.get_or_create(info)
