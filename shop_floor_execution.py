
# DISPATCH MODULE

from datetime import datetime, date

# Global storage
job_counter = 1
batches = {}  # Stores all batches



# Routing Configuration

def get_routing_map(product_type):
    routing_config = {
        "Paracetamol 500mg": [
            "WEIGHING",
            "MIXING",
            "GRANULATION",
            "COMPRESSION",
            "QUALITY_CHECK_1",
            "COATING",
            "PACKAGING"
        ]
    }

    return routing_config.get(product_type)



# Job ID Generator

def generate_job_id(product_type):
    global job_counter

    product_code = "PARA500"  
    job_id = f"{product_code}-BATCH-{str(job_counter).zfill(3)}"

    job_counter += 1
    return job_id


# Input Validation

def validate_order(product_type, quantity, deadline):
    if not product_type:
        return False, "Product type required."

    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    routing = get_routing_map(product_type)
    if routing is None:
        return False, "Routing not defined for product."

    if not deadline:
        return False, "Deadline required."

    # ---- NEW DEADLINE VALIDATION ----
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    except ValueError:
        return False, "Deadline must be in YYYY-MM-DD format."

    today = date.today()

    if deadline_date < today:
        return False, "Deadline cannot be before today."

    return True, "Valid order."




# Create Batch

def create_batch(product_type, quantity, deadline):
    is_valid, message = validate_order(product_type, quantity, deadline)

    if not is_valid:
        print("Order Creation Failed:", message)
        return None

    job_id = generate_job_id(product_type)
    routing = get_routing_map(product_type)

    batch = {
        "job_id": job_id,
        "product_type": product_type,
        "quantity": quantity,
        "deadline": deadline,
        "routing_map": routing.copy(),
        "status": "CREATED"
    }

    batches[job_id] = batch

    print("Batch Created:", job_id)
    return batch


# Release Batch

def release_batch(job_id):
    batch = batches.get(job_id)

    if batch is None:
        print("Batch not found.")
        return None

    if batch["status"] != "CREATED":
        print("Batch cannot be released. Current status:", batch["status"])
        return None

    batch["status"] = "RELEASED"

    print("Batch Released:", job_id)
    return batch


# Cancel Batch (Before Release)

def cancel_batch(job_id):
    batch = batches.get(job_id)

    if batch is None:
        print("Batch not found.")
        return

    if batch["status"] == "RELEASED":
        print("Cannot cancel released batch.")
        return

    batch["status"] = "CANCELLED"
    print("Batch Cancelled:", job_id)


# Get Released Batch for WIP

def get_released_batch(job_id):
    batch = batches.get(job_id)

    if batch and batch["status"] == "RELEASED":
        return batch

    print("Batch not ready for WIP.")
    return None


# View All Batches

def list_batches():
    for job_id, batch in batches.items():
        print(job_id, " ", batch["status"])


# Main Execution

def main():
    product = input("Enter product type: ")
    quantity = int(input("Enter quantity: "))
    deadline = input("Enter deadline: ")

    batch = create_batch(product, quantity, deadline)

    if batch:
        release_batch(batch["job_id"])

    list_batches()


if __name__ == "__main__":
    main()


