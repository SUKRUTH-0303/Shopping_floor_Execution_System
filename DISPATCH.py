# DISPATCH MODULE


class DispatchModule:

    job_counter = 1
    batches = {}

    # Routing Configuration
    @staticmethod
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
    @classmethod
    def generate_job_id(cls, product_type):
        product_code = "PARA500"
        job_id = f"{product_code}-BATCH-{str(cls.job_counter).zfill(3)}"

        cls.job_counter += 1
        return job_id


    # Input Validation
    @classmethod
    def validate_order(cls, product_type, quantity, deadline):

        if not product_type:
            return False, "Product type required."

        if quantity <= 0:
            return False, "Quantity must be greater than zero."

        routing = cls.get_routing_map(product_type)
        if routing is None:
            return False, "Routing not defined for product."

        if not deadline:
            return False, "Deadline required."

        return True, "Valid order."

    # Create Batch
    @classmethod
    def create_batch(cls, product_type, quantity, deadline):

        is_valid, message = cls.validate_order(product_type, quantity, deadline)

        if not is_valid:
            print("Order Creation Failed:", message)
            return None

        job_id = cls.generate_job_id(product_type)
        routing = cls.get_routing_map(product_type)

        # Using list comprehension instead of copy()
        routing_copy = [step for step in routing]

        batch = {
            "job_id": job_id,
            "product_type": product_type,
            "quantity": quantity,
            "deadline": deadline,
            "routing_map": routing_copy,
            "status": "CREATED"
        }

        cls.batches[job_id] = batch

        print("Batch Created:", job_id)
        return batch

    # Release Batch
    @classmethod
    def release_batch(cls, job_id):

        batch = cls.batches.get(job_id)

        if batch is None:
            print("Batch not found.")
            return None

        if batch["status"] != "CREATED":
            print("Batch cannot be released. Current status:", batch["status"])
            return None

        batch["status"] = "RELEASED"

        print("Batch Released:", job_id)
        return batch

    # Cancel Batch
    @classmethod
    def cancel_batch(cls, job_id):

        batch = cls.batches.get(job_id)

        if batch is None:
            print("Batch not found.")
            return

        if batch["status"] == "RELEASED":
            print("Cannot cancel released batch.")
            return

        batch["status"] = "CANCELLED"
        print("Batch Cancelled:", job_id)

    # Get Released Batch
    @classmethod
    def get_released_batch(cls, job_id):

        batch = cls.batches.get(job_id)

        if batch and batch["status"] == "RELEASED":
            return batch

        print("Batch not ready for WIP.")
        return None

    # View All Batches
    @classmethod
    def list_batches(cls):

        # Using for loop (clear & readable)
        for job_id, batch in cls.batches.items():
            print(job_id, " ", batch["status"])


# Main Execution
def main():

    product = input("Enter product type: ")
    quantity = int(input("Enter quantity: "))
    deadline = input("Enter deadline: ")

    batch = DispatchModule.create_batch(product, quantity, deadline)

    if batch:
        DispatchModule.release_batch(batch["job_id"])

    DispatchModule.list_batches()


if __name__ == "__main__":
    main()