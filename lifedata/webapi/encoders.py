from typing import Any

import numpy as np
import orjson
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def orjsonable_encoder(obj: Any, **kwargs: dict) -> Any:
    """
    Use this instead of ``pydantic.encoders.jsonable_encoder`` together with
    ``ORJSONNumpyResponse``. See there for more information.
    """
    custom_encoder = kwargs.pop("custom_encoder", {})
    if np.ndarray not in custom_encoder:
        # Don't do anything with the numpy array. This will be later handled by
        # orjson.
        custom_encoder[np.ndarray] = lambda v: v
    return jsonable_encoder(obj, custom_encoder=custom_encoder, **kwargs)


class ORJSONNumpyResponse(JSONResponse):
    """
    Allow serializing numpy arrays to JSON lists.

    When using that in a FastAPI path operation, you need to pass the
    to-be-serialized data through ``orjsonable_encoder`` first. Otherwise
    FastAPI will complain about the contained numpy data.

    Example::

        @app.get("/', response_class=ORJSONNumpyResponse)
        def my_operation():
            return orjsonable_encoder({
                "values": np.array([1, 2, 3]),
            })
    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY)
