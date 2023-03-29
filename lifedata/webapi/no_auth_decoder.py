from dataclasses import dataclass

from lifedata.annotations.annotator import UserInfo

ANONYMOUS_USER = UserInfo(
    id="anonymous", name="Anonymous", email="anonymous@example.com"
)


@dataclass
class NoAuthDecoder:
    user: UserInfo = ANONYMOUS_USER

    def decode(self, token: str) -> UserInfo:
        return self.user
