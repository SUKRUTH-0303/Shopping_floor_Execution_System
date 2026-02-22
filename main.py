# MAIN ORCHESTRATOR
# Dispatch → Tracking (WIP) → Quality

import time
from DISPATCH import DispatchModule
import Tracking as WIP
import quality


class ShopFloorSystem:
    def __init__(self) -> None:
        self.job_id: str | None = None
        self.qc = quality.QualityControl()

    def simulate_processing(self, station: str) -> None:
        print(f"\n{station} STARTED")
        for _ in range(3):
            print(f"{station} processing................")
            time.sleep(1)
        print(f"{station} COMPLETED")

    def get_user_input(self) -> tuple[str, int, str] | None:
        product: str = input(
            "Enter Product Type (example: Paracetamol 500mg): "
        ).strip()

        quantity_input: str = input("Enter Target Quantity: ").strip()
        deadline: str = input("Enter Deadline (YYYY-MM-DD): ").strip()

        try:
            quantity: int = int(quantity_input)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Invalid quantity. Please enter a positive integer.")
            return None

        return product, quantity, deadline

    def process_flow(self) -> None:
        if self.job_id is None:
            return

        batch_obj: WIP.Batch = WIP.batches[self.job_id]

        while True:
            status: str = batch_obj.status

            if status == "FINISHED":
                print("\nPRODUCTION COMPLETED SUCCESSFULLY")
                break

            if status == "UNDER_INSPECTION":
                self.qc.start_quality(batch_obj)
                continue

            if status.startswith("READY_AT_"):
                station: str = batch_obj.routing_map[batch_obj.current_step]

                input(f"\nPress ENTER to start {station}...")
                batch_obj.start_station()

                self.simulate_processing(station)
                batch_obj.finish_station()
                continue

            if status == "QUARANTINED":
                print("\nBATCH FAILED QUALITY. PROCESS STOPPED.")
                break

    def run(self) -> None:
        print("\n===== SHOP FLOOR EXECUTION SYSTEM =====\n")

        user_input = self.get_user_input()
        if user_input is None:
            return

        product, total_quantity, deadline = user_input

        batch_size: int = 100
        remaining: int = total_quantity
        created_jobs: list[str] = []

        while remaining > 0:
            current_qty: int = min(batch_size, remaining)

            batch_dict = DispatchModule.create_batch(
                product, current_qty, deadline
            )

            if batch_dict is None:
                print("Batch creation failed.")
                return

            DispatchModule.release_batch(batch_dict["job_id"])

            created_jobs.append(batch_dict["job_id"])
            remaining -= current_qty

        for job_id in created_jobs:
            dispatch_batch = DispatchModule.batches[job_id]

            routing_map = dispatch_batch["routing_map"]

            batch_obj = WIP.Batch(job_id, routing_map)
            batch_obj.release()
            batch_obj.receive()

            WIP.batches[job_id] = batch_obj

        for job_id in created_jobs:
            print(f"\n===== PROCESSING BATCH {job_id} =====")
            self.job_id = job_id
            self.process_flow()


if __name__ == "__main__":
    system = ShopFloorSystem()
    system.run()
