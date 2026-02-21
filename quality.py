import WIP

Number = int | float

quality_results: dict[str, "QualityRecord"] = {}

class QualityRecord:
    def __init__(self, hardness: Number, friability: Number, dissolution: Number) -> None:
        self.hardness: float = float(hardness)
        self.friability: float = float(friability)
        self.dissolution: float = float(dissolution)


def start_quality(job_id: str) -> None:
    batch: dict[str, object] | None = WIP.batches.get(job_id)

    if batch is None:
        print("Job not found:", job_id)
        return

    if batch["status"] != "UNDER_INSPECTION":  
        print("Job is not ready for quality inspection")
        return

    print("\n--- QUALITY CHECK STARTED ---")
    print("Job:", job_id)

    try:
        hardness: Number = float(input("Enter Hardness (kg/cm2): "))
        friability: Number = float(input("Enter Friability (%): "))
        dissolution: Number = float(input("Enter Dissolution (%): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    record = QualityRecord(hardness, friability, dissolution)
    quality_results[job_id] = record

    evaluate(job_id)

def evaluate(job_id: str) -> None:
    record: QualityRecord | None = quality_results.get(job_id)

    if record is None:
        print("No quality data found")
        return

    if (
        record.hardness >= 4
        and record.friability <= 1
        and record.dissolution >= 80
    ):
        pass_batch(job_id)
    else:
        fail(job_id)

def pass_batch(job_id: str) -> None:
    print("QUALITY PASSED")
    WIP.release_hold(job_id)

def fail(job_id: str) -> None:
    print("QUALITY FAILED")
    WIP.quarantine(job_id)

def view_results(job_id: str) -> None:
    record: QualityRecord | None = quality_results.get(job_id)

    if record is None:
        print("No quality record found")
        return

    print("\nQUALITY REPORT")
    print("Hardness:", record.hardness)
    print("Friability:", record.friability)
    print("Dissolution:", record.dissolution)
