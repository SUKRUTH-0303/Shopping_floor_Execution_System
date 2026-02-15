import time
import shop_floor_execution as dispatch
import WIP
import quality

def simulate_processing(station):
    print("\n", station, "STARTED")
    for i in range(3):
        print(station, "processing...")
        time.sleep(1)
    print(station, "COMPLETED")

def main():
    print("\n===== SHOP FLOOR EXECUTION SYSTEM =====\n")
    
    # get batch details from user
    product = input("Enter Product Type (example: Paracetamol 500mg): ")
    quantity = int(input("Enter Target Quantity: "))
    deadline = input("Enter Deadline (YYYY-MM-DD): ")
    
    batch = dispatch.create_batch(product, quantity, deadline)
    if batch is None:
        return
    
    dispatch.release_batch(batch["job_id"])
    
    # share batch data with WIP module
    WIP.batches = dispatch.batches
    job_id = batch["job_id"]
    
    WIP.receive_job(job_id)
    
    # main processing loop
    while True:
        batch = WIP.batches[job_id]
        status = batch["status"]
        
        if status == "FINISHED":
            print("\n PRODUCTION COMPLETED SUCCESSFULLY")
            break

        if status == "UNDER_INSPECTION":
            quality.start_quality(job_id)
            continue

        if status.startswith("READY_AT_"):
            station = batch["routing_map"][batch["current_step"]]
            
            input("\nPress ENTER to start " + station + "...")
            WIP.start_station(job_id)
            
            simulate_processing(station)
            WIP.finish_station(job_id)
            
            continue

        if status == "QUARANTINED":
            print("\n BATCH FAILED QUALITY. PROCESS STOPPED.")
            break


if __name__ == "__main__":
    main()