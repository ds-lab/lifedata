from pathlib import Path
from typing import Any
from typing import Optional
from typing import Union


class SampleView:
    """
    Custom component to render samples in the annotation UI.
    Use this object to configure how the sample view will be provided to
    the frontend.
    """

    def __init__(
        self,
        name: str = None,  # type: ignore
        directory: Union[str, Path, None] = None,
        url: Optional[str] = None,
        args: Optional[Any] = None,
    ):
        assert [name, directory, url].count(
            None
        ) == 2, "Expected exactly one of `name` or `directory` or `url` to be set"

        self.name = name
        self.directory = Path(directory) if directory is not None else None
        self.url = url
        self.args = args

        if self.directory is not None:
            assert (
                self.directory.is_dir()
            ), f"Expected {self.directory} to be a directory"
