from . import models
from .database import Session
from lifedata.annotations.annotator import Annotator
from lifedata.annotations.annotator import AnnotatorRepository
from lifedata.annotations.annotator import UserInfo
from lifedata.annotations.events import EventDispatcher


class AnnotatorDBRepository(AnnotatorRepository):
    def __init__(self, db: Session, event_dispatcher: EventDispatcher):
        self._db = db
        super().__init__(event_dispatcher=event_dispatcher)

    def _instantiate(self, model: models.Annotator) -> Annotator:
        return Annotator(
            id=model.id, name=model.name, email=model.email, formal_training=[]
        )

    def by_id(self, id: str) -> Annotator:
        instance = self._db.query(models.Annotator).filter_by(id=id).first()
        if instance is None:
            raise self.NotFound(f"No annotator with id={id}")
        return self._instantiate(instance)

    def create(self, info: UserInfo) -> Annotator:
        model = models.Annotator(id=info.id, name=info.name, email=info.email)
        self._db.add(model)
        return self._instantiate(model)
