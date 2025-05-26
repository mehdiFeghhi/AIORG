import csv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.job_performance.job_performance import JobPerformance

# مسیر فایل CSV
CSV_PATH = "output_csv/all_labels.csv"

def load_performances():
    db: Session = SessionLocal()
    try:
        with open(CSV_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                person_id = int(row["ID"])
                job_efficiency_rank = int(row["Work Impact"])
                improvement_rank = int(row["Career Growth"])
                satisfaction_score = float(row["Job Satisfaction"])
                job_id = 1
                shamsi_year = int(row["Shamsi Year"])  # فرض: "1402"
                created_at = f"{shamsi_year}/01/01"  # مثلاً '1402/01/01'

                JobPerformance.add_performance(
                    db,
                    person_id,
                    job_efficiency_rank,
                    improvement_rank,
                    satisfaction_score,
                    job_id,
                    created_at
                )
        db.commit()
        print("✅ Done importing job performances.")
    except Exception as e:
        print("❌ Error:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_performances()
