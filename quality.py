import Tracking

Number = int | float

class QualityRecord:
    def __init__(self, hardness: Number, friability: Number, dissolution: Number) -> None:
        self.hardness: float = float(hardness)
        self.friability: float = float(friability)
        self.dissolution: float = float(dissolution)

class QualityControl:
    def __init__(self) -> None:
        self.quality_results: dict[str, QualityRecord] = {}

    def start_quality(self, batch: Tracking.Batch) -> None:
        if batch.status != "UNDER_INSPECTION":
            print("Job is not ready for quality inspection")
            return

        print("\n--- QUALITY CHECK STARTED ---")
        print("Job:", batch.job_id)

        try:
            hardness: Number = float(input("Enter Hardness (kg/cm2): "))
            friability: Number = float(input("Enter Friability (%): "))
            dissolution: Number = float(input("Enter Dissolution (%): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return

        record = QualityRecord(hardness, friability, dissolution)
        self.quality_results[batch.job_id] = record

        self._evaluate(batch)

    def _evaluate(self, batch: Tracking.Batch) -> None:
        record: QualityRecord | None = self.quality_results.get(batch.job_id)

        if record is None:
            print("No quality data found")
            return

        if (
            record.hardness >= 4
            and record.friability <= 1
            and record.dissolution >= 80
        ):
            self._pass_batch(batch)
        else:
            self._fail(batch)

    def _pass_batch(self, batch: Tracking.Batch) -> None:
        print("QUALITY PASSED")
        batch.release_hold()

    def _fail_batch(self, batch: Tracking.Batch) -> None:
        print("QUALITY FAILED")
        batch.quarantine()

    # Corrected internal method name
    def _fail(self, batch: Tracking.Batch) -> None:
        self._fail_batch(batch)

    def view_results(self, batch: Tracking.Batch) -> None:
        record: QualityRecord | None = self.quality_results.get(batch.job_id)

        if record is None:
            print("No quality record found")
            return

        print("\nQUALITY REPORT")
        print("Hardness:", record.hardness)
        print("Friability:", record.friability)
        print("Dissolution:", record.dissolution)
