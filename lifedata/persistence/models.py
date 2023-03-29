from sqlalchemy import ARRAY
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .database import Base

# When modifying the database models, make sure to create a migration using:
#     alembic revision --autogenerate -m "your change message"


class Annotator(Base):
    __tablename__ = "annotators"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(250))
    email = Column(String(250))

    def __str__(self) -> str:
        return f"Annotator(id={self.id} name={self.name})"


class Sample(Base):
    __tablename__ = "samples"

    id = Column(String, primary_key=True, index=True)
    created = Column(DateTime, default=func.now())

    queriedsample = relationship("QueriedSample", back_populates="sample")
    assignments = relationship("Assignment", back_populates="sample")
    annotations = relationship("Annotation", back_populates="sample")
    annotationqueue = relationship("AnnotationQueue", back_populates="sample")
    skippedsamples = relationship("Skipped", back_populates="sample")

    def __str__(self) -> str:
        return f"Sample(id={self.id})"


class QueriedSample(Base):
    """
    NOTE: The state of labeled and unlabeled samples can be determined from Annotation
    Sample in Annotation = labeled | Sample not in Annotation = unlabeled
    NOTE: Samples that are currently annotated can be found out via Assignment and Annotation
    Sample not in Annotation &  Sample in Assignment = currently annotated
    """

    __tablename__ = "queriedsamples"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("samples.id"), index=True)
    query_index = Column(Integer, index=True)

    sample = relationship("Sample", back_populates="queriedsample")


class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True, index=True)
    annotator_id = Column(String, index=True)
    sample_id = Column(String, ForeignKey("samples.id"), index=True)
    created = Column(DateTime, default=func.now())

    sample = relationship("Sample", back_populates="assignments")


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("samples.id"), index=True, nullable=False)
    annotator_id = Column(String, index=True)
    labels = Column(ARRAY(String))
    created = Column(DateTime, default=func.now())

    sample = relationship("Sample", back_populates="annotations")


class AnnotationQueue(Base):
    __tablename__ = "annotationqueue"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("samples.id"), index=True, nullable=False)
    queue_name = Column(String, nullable=False)
    requested_by = Column(String, index=True)
    created = Column(DateTime, default=func.now())

    sample = relationship("Sample", back_populates="annotationqueue")


class Skipped(Base):
    __tablename__ = "skippedsamples"

    id = Column(Integer, primary_key=True, index=True)
    sample_id = Column(String, ForeignKey("samples.id"), index=True, nullable=False)
    annotator_id = Column(String, index=True)
    created = Column(DateTime, default=func.now())

    sample = relationship("Sample", back_populates="skippedsamples")


class EventLog(Base):
    __tablename__ = "eventlog"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    payload = Column(JSON, nullable=False)
    recorded = Column(DateTime, nullable=False)
    stored = Column(DateTime, nullable=False, default=func.now())

    def __str__(self) -> str:
        return f"EventLog({self.name}@{self.sampled})"
