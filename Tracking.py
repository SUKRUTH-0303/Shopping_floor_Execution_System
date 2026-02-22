class Batch:
    def __init__(self, job_id: str, routing_map: list[str]) -> None:
        if not routing_map:
            print("Routing map cannot be empty")
            return

        self.job_id: str = job_id
        self.routing_map: list[str] = routing_map
        self.current_step: int = 0
        self.status: str = "CREATED"

    def release(self) -> None:
        if self.status != "CREATED":
            print("Batch already released or in progress")
            return
        self.status = "RELEASED"

    def receive(self) -> None:
        if self.status != "RELEASED":
            print("Batch is not in RELEASED state")
            return

        first_station: str = self.routing_map[0]
        self.current_step = 0
        
        if "LAB_TEST" in first_station or "QUALITY_CHECK" in first_station:
            self.status = "UNDER_INSPECTION"
        else:
            self.status = "READY_AT_" + first_station

    def start_station(self) -> None:
        if not self.status.startswith("READY_AT_"):
            print("Batch is not ready to start")
            return

        station: str = self.routing_map[self.current_step]
        self.status = "IN_PROGRESS_" + station
        
    def finish_station(self) -> None:
        if not self.status.startswith("IN_PROGRESS_"):
            print("Batch is not in progress")
            return

        self.advance_to_next()

    def release_hold(self) -> None:
        if self.status != "UNDER_INSPECTION":
            print("Batch not under inspection")
            return

        self.advance_to_next()

    def quarantine(self) -> None:
        if self.status != "UNDER_INSPECTION":
            print("Batch not under inspection")
            return

        self.status = "QUARANTINED"

    def advance_to_next(self) -> None:
        next_index: int = self.current_step + 1

        if next_index >= len(self.routing_map):
            self.status = "FINISHED"
            return

        next_station: str = self.routing_map[next_index]
        self.current_step = next_index

        if "LAB_TEST" in next_station or "QUALITY_CHECK" in next_station:
            self.status = "UNDER_INSPECTION"
        else:
            self.status = f"READY_AT_{next_station}"

    def get_status(self) -> None:
        station: str = self.routing_map[self.current_step]
        print(f"Job: {self.job_id} | Status: {self.status} | Station: {station}")

# Global dictionary to hold tracking batches as expected by main.py
batches: dict[str, Batch] = {}