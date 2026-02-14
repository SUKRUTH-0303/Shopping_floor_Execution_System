# Global storage - initialized from shop_floor_execution.py
batches = {}

def receive_job(job_id):
    # Accept a released batch into production.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    if batch["status"] != "RELEASED":
        print("Job", "needs to be released first")
        return

    first_station = batch["routing_map"][0]
    batch["current_step"] = 0
    batch["status"] = "READY_AT_" + first_station
    print("Job", "received. Status:", batch["status"])


def start_station(job_id):
    # Start work at the current station.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    # check if the job is actually ready
    if not batch["status"].startswith("READY_AT_"):
        print("Job", "is not ready to start. Current status:", batch["status"])
        return

    station = batch["routing_map"][batch["current_step"]]
    batch["status"] = "IN_PROGRESS_" + station
    print("Job", "- started work at", station)


def finish_station(job_id):
    # Finish work at the current station and move to next.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    if not batch["status"].startswith("IN_PROGRESS_"):
        print("Job", "is not in progress right now")
        return

    station = batch["routing_map"][batch["current_step"]]
    print("Job", "- finished", station)

    # now move to the next step
    advance_to_next(batch)


def advance_to_next(batch):
    # Move the batch to the next station in the route.
    job_id = batch["job_id"]
    next_index = batch["current_step"] + 1

    # check if all stations are done
    if next_index >= len(batch["routing_map"]):
        batch["status"] = "FINISHED"
        print("Job", "is FINISHED! All stations complete.")
        return

    next_station = batch["routing_map"][next_index]
    batch["current_step"] = next_index

    # if next station is a lab test or quality check, lock the batch
    if "LAB_TEST" in next_station or "QUALITY_CHECK" in next_station:
        batch["status"] = "UNDER_INSPECTION"
        print("Job", "is now UNDER INSPECTION at", next_station)
        print("Batch is locked. Waiting for quality team to release it.")
        return

    # otherwise just move to the next station
    batch["status"] = "READY_AT_" + next_station
    print("Job","- moved to", next_station)


def release_hold(job_id):
    # Quality team approved - release the batch.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    if batch["status"] != "UNDER_INSPECTION":
        print("Job", "is not under inspection")
        return

    print("Job", "- quality PASSED, releasing hold")
    advance_to_next(batch)


def quarantine(job_id):
    # Quality team rejected - quarantine the batch.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    if batch["status"] != "UNDER_INSPECTION":
        print("Job", "is not under inspection")
        return

    batch["status"] = "QUARANTINED"
    print("Job", "is QUARANTINED")


def get_status(job_id):
    # Print the current status of a batch.
    batch = batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    station = batch["routing_map"][batch["current_step"]]
    print("Job:", job_id, "| Status:", batch["status"], "| Station:", station)