from .lifedata_api.api import lifedata_api_instance


def __getattr__(name):
    # Loading the project instance, when the project module variable is requested.
    # This supports the usage of
    #     from lifedata import project
    if name == "project":
        if "project" not in globals():
            globals()["project"] = lifedata_api_instance()
        return globals()["project"]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
