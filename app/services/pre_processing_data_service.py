from app.models.job_performance.job_performance import JobPerformance
from app.models.files.data_file import DataFile
from app.schemas import data_loader
import pandas as pd
import numpy as np


def make_dataset(job_id: str, exam_id: str, performance_metric: str, db):
    """
    Creates a dataset by finding similar job IDs and aggregating performance and file data.

    Args:
        job_id (str): The ID of the base job to find similar jobs for.
        exam_id (str): The ID of the exam to retrieve file data for.
        performance_metric (str): The performance metric to retrieve for each job.
            Accepted values: 'job_efficiency_rank', 'improvement_rank', 'satisfaction_score'.
        db (Session): SQLAlchemy database session to interact with the database.

    Returns:
        tuple: A tuple containing:
            - X (pd.DataFrame): Features dataset.
            - Y (pd.Series): Labels dataset corresponding to the performance metric.
    """
    # Step 1: Find all similar job IDs
    list_of_job_id = find_all_similar_job(job_id)

    # Step 2: Retrieve performance data grouped by year
    performance_data = fetch_performance_data(db, list_of_job_id, performance_metric)

    # Step 3: Retrieve files grouped by Persian calendar year
    date_files_dict = fetch_file_data(db, exam_id)

    # Step 4: Process and combine features and labels
    X, Y = process_data(performance_data, date_files_dict, performance_metric)

    return X,Y


    

def fetch_performance_data(db, job_ids, performance_metric):
    """Retrieve performance data grouped by year."""
    return JobPerformance.get_performance_by_jobs_and_date(
        db=db,
        job_ids=job_ids,
        performance_metric=performance_metric
    )


def fetch_file_data(db, exam_id):
    """Retrieve files grouped by Persian calendar year."""
    return DataFile.get_files_by_exam_id(db=db, exam_id=exam_id)


def process_data(performance_data, date_files_dict, performance_metric:str):
    """Process and combine features and labels from performance and file data."""
    combined_features = []
    combined_labels = []

    for year, records in performance_data.items():
        if year in date_files_dict:
            for file_path in date_files_dict[year]:
                try:
                    combined_features, combined_labels = process_file(
                        file_path, records, combined_features, combined_labels
                    )
                except Exception as e:
                    print(f"Error loading file {file_path}: {e}")

    # Convert to pandas DataFrame and Series
    X = pd.DataFrame(combined_features)
    Y = pd.Series(combined_labels, name=performance_metric)

    return X, Y


def process_file(file_path, records, combined_features, combined_labels):
    """Process a single file and update combined features and labels."""
    # Load the CSV file
    data_df = pd.read_csv(file_path)

    # Filter the data for person IDs present in the performance records
    person_ids = {record['person_id'] for record in records}
    filtered_data = data_df[data_df['person_id'].isin(person_ids)]

    # Combine the filtered data with performance values
    for record in records:
        person_id = record['person_id']
        performance_value = record['performance_value']

        # Extract relevant features for the person
        person_features = filtered_data[filtered_data['person_id'] == person_id]
        if not person_features.empty:
            # Append features and label
            combined_features.append(person_features.drop(columns=['person_id']).values.flatten())
            combined_labels.append(performance_value)

    return combined_features, combined_labels






def find_all_similar_job(job_id):

    ### TODO I Must write query for this
    return [job_id]