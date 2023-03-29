from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import Optional

import jwt
from jwt.jwks_client import PyJWKClient
from pydantic import BaseModel

from .no_auth_decoder import ANONYMOUS_USER
from lifedata.annotations.annotator import UserInfo


class JwtToken(BaseModel):
    sub: str
    email: str
    family_name: Optional[str]
    given_name: Optional[str]
    name: Optional[str]


@dataclass
class KeycloakJwtDecoder:
    """
    ``audience`` needs to match the audience set in the token. For default setup
    in keycloak this is ``"account"``.

    ``jwks_uri`` is the URL where the JWKS keys can be retrieved. For keycloak this is
    ``https://.../auth/realms/lifedata/protocol/openid-connect/certs``
    """

    audience: str
    jwks_uri: str
    allow_anonymous_user_for_empty_token: bool = False
    anonymous_user: UserInfo = ANONYMOUS_USER
    jwt_decode_options: Dict[str, bool] = field(default_factory=dict)

    def get_jwks_client(self) -> PyJWKClient:
        if not hasattr(self, "_jwks_client"):
            self._jwks_client = PyJWKClient(self.jwks_uri)
        return self._jwks_client

    def decode(self, token: str) -> UserInfo:
        if token == "" and self.allow_anonymous_user_for_empty_token:
            return self.anonymous_user

        jwks_client = self.get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded_token = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=[self.audience],
            options=self.jwt_decode_options,
        )
        validated_token = JwtToken(**decoded_token)
        return UserInfo(
            id=validated_token.sub,
            name=validated_token.name or "",
            email=validated_token.email,
        )
