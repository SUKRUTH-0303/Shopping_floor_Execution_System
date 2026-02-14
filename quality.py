import WIP
quality_results = {}


def start_quality(job_id):

    batch = WIP.batches.get(job_id)
    if batch is None:
        print("Job not found:", job_id)
        return

    if batch["status"] != "UNDER_INSPECTION":
        print("Job is not ready for quality inspection")
        return

    print("\n QUALITY CHECK STARTED! ")
    print("Job:", job_id)

    hardness = float(input("Enter Hardness (kg/cm2): "))
    friability = float(input("Enter Friability (%): "))
    dissolution = float(input("Enter Dissolution (%): "))

    result = {
        "hardness": hardness,
        "friability": friability,
        "dissolution": dissolution
    }

    quality_results[job_id] = result

    evaluate(job_id)


def evaluate(job_id):
    # Decide PASS / FAIL

    record = quality_results.get(job_id)

    if record is None:
        print("No quality data")
        return

    if record["hardness"] < 4:
        fail(job_id)
        return

    if record["friability"] > 1:
        fail(job_id)
        return

    if record["dissolution"] < 80:
        fail(job_id)
        return
    pass_batch(job_id)

def pass_batch(job_id):
    print("QUALITY PASSED")
    WIP.release_hold(job_id)


def fail(job_id):
    print("QUALITY FAILED")
    WIP.quarantine(job_id)


def view_results(job_id):
    record = quality_results.get(job_id)

    if record is None:
        print("No quality record found")
        return

    print("\nQUALITY REPORT")
    for k, v in record.items():
        print(k, ":", v)
