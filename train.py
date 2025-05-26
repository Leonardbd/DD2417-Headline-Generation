from openai import OpenAI
import time
import sys

client = OpenAI(api_key="sk-...") #Your API-key here


log_file_path = "finetune_log.txt"


def log(msg):
    print(msg)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


with open(log_file_path, "w", encoding="utf-8") as f:
    f.write("Starting fine-tuning log\n")


train_file_resp = client.files.create(
    file=open("data\\headlines_train.jsonl", "rb"),
    purpose="fine-tune"
)
val_file_resp = client.files.create(
    file=open("data\\headlines_val.jsonl", "rb"),
    purpose="fine-tune"
)

log(f"Training file ID: {train_file_resp.id}")
log(f"Validation file ID: {val_file_resp.id}")

#Grid search parameters
batch_sizes = [2, 4]
lr_multipliers = [2, 3]
num_epochs = [2, 3]

for batch_size in batch_sizes:
    for lr_mult in lr_multipliers:
        for epochs in num_epochs:
            log(f"\nStarting fine-tune job: batch_size={batch_size}, lr_mult={lr_mult}, epochs={epochs}")
            response = client.fine_tuning.jobs.create(
                model="gpt-4.1-mini-2025-04-14",
                training_file=train_file_resp.id,
                validation_file=val_file_resp.id,
                hyperparameters={
                    "batch_size": batch_size,
                    "learning_rate_multiplier": lr_mult,
                    "n_epochs": epochs
                }
            )
            job_id = response.id
            log(f"Started job {job_id}")

            #Wait for this job to complete before starting the next
            while True:
                job = client.fine_tuning.jobs.retrieve(job_id)
                status = job.status
                log(f"Job {job_id} status: {status}")
                if status in ["succeeded", "failed", "cancelled"]:
                    log(f"Job {job_id} finished with status: {status}")
                    break
                time.sleep(60)

log("\nAll fine-tuning jobs have completed!")
