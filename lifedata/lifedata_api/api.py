from .load_lifedata_api import load_project_api
from .load_lifedata_api import Project

project: Project


def lifedata_api_instance() -> Project:
    return Project(load_project_api())
