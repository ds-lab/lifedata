import collections
import sys
from datetime import datetime
from typing import List
from typing import Optional

import click
import numpy as np
import pandas as pd
from fastapi.encoders import jsonable_encoder
from loguru import logger

from ..annotations.annotation import Annotation
from lifedata.cli.configure_db import db_option
from lifedata.cli.main import main
from lifedata.persistence.annotation_db_repository import AnnotationsDBRepository
from lifedata.persistence.database import configure_database
from lifedata.persistence.database import Session


def split_annotations(samples_labeled: pd.DataFrame) -> pd.DataFrame:
    """
    Split labels from single row to multiple rows
    """
    return samples_labeled.assign(labels=samples_labeled.labels).explode("labels")


def count_annotations(annotation_objects: List[Annotation]) -> collections.Counter:
    """
    Determines which label was labelled how many times
    """
    annotations_separated = []
    for annotation in annotation_objects:
        annotations_separated.append(annotation.labels)
    annotations_flattened = [
        item for sublist in annotations_separated for item in sublist
    ]

    return collections.Counter(annotations_flattened)


@main.group(invoke_without_command=True)
def analyse() -> None:
    """
    Commands to analyse data
    """
    pass


@analyse.command()
@db_option()
@click.option(
    "--interval-start-time",
    "interval_start_time",
    type=click.DateTime(
        formats=[
            "%Y-%m-%d",
            "%Y-%m-%d %H",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
        ]
    ),
    default=None,
)
@click.option(
    "--interval-stop-time",
    "interval_stop_time",
    type=click.DateTime(
        formats=[
            "%Y-%m-%d",
            "%Y-%m-%d %H",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
        ]
    ),
    default=None,
)
def label_frequency(
    db: str,
    interval_start_time: Optional[datetime],
    interval_stop_time: Optional[datetime],
) -> None:
    """
    Dump label frequency to console. By default, all labels are dumped. With specification of an interval-start-time all annotations after this time are dumped.
    """
    configure_database(db)
    session = Session()
    annotation_db_repository = AnnotationsDBRepository(session)

    if interval_start_time:
        logger.info(f"Dump labels after {interval_start_time}")
    if interval_stop_time:
        logger.info(f"Dump labels before {interval_stop_time}")

    queried_result = annotation_db_repository.query_labeled(
        interval_start_time, interval_stop_time
    )
    annotations_counted = count_annotations(queried_result)

    label_frequency = {"label_frequency": dict(annotations_counted)}

    label_frequency = jsonable_encoder(label_frequency)

    sys.stdout.write(f"{label_frequency}\n")


@analyse.command()
@db_option()
@click.option(
    "--percent",
    "-p",
    "percentage_result",
    is_flag=True,
    help="Use -p to get the percentage result instead of frequency",
)
def label_cooccurrence(db: str, percentage_result: bool) -> None:
    """
    Command to get heatmap coefficients for label cooccurrence
    """

    def as_dict(annotation_object):
        return {
            "sample_id": annotation_object.sample_id,
            "labels": annotation_object.labels,
            "created": annotation_object.created,
        }

    configure_database(db)
    session = Session()
    annotation_db_repository = AnnotationsDBRepository(session)

    queried_result = annotation_db_repository.query_labeled()

    if not queried_result:
        sys.stdout.write(
            "Actually there are no samples to analyse. Please do some annotations first\n"
        )
        return

    labeled_df = pd.DataFrame([as_dict(x) for x in queried_result])
    splitted_labeled_df = split_annotations(labeled_df)

    unique_labels = splitted_labeled_df.labels.unique()
    labels_max = splitted_labeled_df.sample_id.value_counts().max()
    label_occurrence_df = pd.DataFrame(
        0, columns=range(1, labels_max + 1), index=unique_labels
    )

    for unique_label in unique_labels:
        # Find sample_ids that include a special label
        sample_ids_with_label = splitted_labeled_df[
            splitted_labeled_df.labels == unique_label
        ].sample_id
        # Get all labels to the found sample_ids
        filtered_for_ids = splitted_labeled_df[
            splitted_labeled_df.sample_id.isin(sample_ids_with_label)
        ]
        # Count how many labels occur with a label
        counted_label_occurrences_for_label = (
            filtered_for_ids.sample_id.value_counts().value_counts()
        )

        # Add results to result dataframe
        label_occurrence_df.loc[unique_label] = label_occurrence_df.loc[
            unique_label
        ].combine(counted_label_occurrences_for_label, max)

    if percentage_result:
        label_occurrence_df_percentage = label_occurrence_df.div(
            label_occurrence_df.sum(axis=1), axis=0
        )
        sys.stdout.write(
            f"{jsonable_encoder(label_occurrence_df_percentage.T.to_dict())}\n"
        )
    else:
        sys.stdout.write(f"{jsonable_encoder(label_occurrence_df.T.to_dict())}\n")


@analyse.command()
@db_option()
@click.option(
    "--percent",
    "-p",
    "percentage_result",
    is_flag=True,
    help="Use -p to get the percentage result instead of frequency",
)
def label_correlation(db: str, percentage_result: bool) -> None:
    """
    Command to analyse label correlation for already annotated samples.
    """

    def as_dict(annotation_object):
        return {
            "sample_id": annotation_object.sample_id,
            "labels": annotation_object.labels,
            "created": annotation_object.created,
        }

    configure_database(db)
    session = Session()
    annotation_db_repository = AnnotationsDBRepository(session)

    queried_result = annotation_db_repository.query_labeled()

    if not queried_result:
        sys.stdout.write(
            "Actually there are no samples to analyse. Please do some annotations first\n"
        )
        return

    labeled_df = pd.DataFrame([as_dict(x) for x in queried_result])
    splitted_labeled_df = split_annotations(labeled_df)
    unique_labels = splitted_labeled_df.labels.unique()
    label_appearance_overall = pd.DataFrame(
        0, columns=unique_labels, index=np.flip(unique_labels)
    )

    for unique_label in unique_labels:
        # Find samples that include the actual unique_label
        tmp_sample_ids = splitted_labeled_df[
            splitted_labeled_df.labels == unique_label
        ].sample_id

        # Filter for all annotations of the samples that include the unique_label
        filtered_for_ids = splitted_labeled_df[
            splitted_labeled_df.sample_id.isin(tmp_sample_ids)
        ]

        # Count label frequency in the found samples that include the unique_label
        tmp_values_count = filtered_for_ids.labels.value_counts()

        # Add the counted labels to label_appearance_overall_percent_df
        label_appearance_overall.loc[unique_label] = label_appearance_overall.loc[
            unique_label
        ].combine(tmp_values_count, max)

        # Correct entries in which the unique_label appears with itself
        only_self_occurrence_samples_df = filtered_for_ids.drop_duplicates(
            subset=["sample_id"], keep=False
        )
        label_appearance_overall[unique_label][unique_label] = len(
            only_self_occurrence_samples_df
        )

    if percentage_result:
        # Calculate the percentage heatmap from label_appearance_overall
        label_appearance_overall_df_percentage = label_appearance_overall.div(
            label_appearance_overall.sum(axis=1), axis=0
        )
        sys.stdout.write(
            f"{jsonable_encoder(label_appearance_overall_df_percentage[label_appearance_overall_df_percentage.columns[::-1]].T.to_dict())}\n"
        )
    else:
        sys.stdout.write(
            f"{jsonable_encoder(label_appearance_overall[label_appearance_overall.columns[::-1]].T.to_dict())}\n"
        )
