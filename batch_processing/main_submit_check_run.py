import sys
from pathlib import Path

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# The last submitted batch ID is saved here so check/results can find it later.
BATCH_ID_FILE = Path(__file__).parent / "batch_id.txt"

ITEMS = [
    "The product quality is excellent!",
    "Terrible customer service, never again.",
    "It's okay, nothing special.",
    "Absolutely love this, best purchase of the year.",
    "Shipping took forever and the box was damaged.",
    "This was best ever, return customer for sure!"
]


def submit(client):
    # custom_id is how you correlate each result back to its input.
    requests = [
        Request(
            custom_id=f"classify-{i}",
            params=MessageCreateParamsNonStreaming(
                model="claude-haiku-4-5",
                max_tokens=20,
                messages=[{
                    "role": "user",
                    "content": f"Classify as positive, negative, or neutral (one word only): {text}",
                }],
            ),
        )
        for i, text in enumerate(ITEMS)
    ]

    batch = client.messages.batches.create(requests=requests)
    BATCH_ID_FILE.write_text(batch.id)
    print(f"Submitted batch {batch.id} (status: {batch.processing_status})")
    print(f"Batch ID saved to {BATCH_ID_FILE.name}. Run 'check' or 'results' later.")


def check(client, batch_id):
    batch = client.messages.batches.retrieve(batch_id)
    counts = batch.request_counts
    print(f"Batch {batch.id}: {batch.processing_status}")
    print(f"  processing: {counts.processing}, succeeded: {counts.succeeded}, "
          f"errored: {counts.errored}, canceled: {counts.canceled}, expired: {counts.expired}")
    return batch


def results(client, batch_id):
    batch = check(client, batch_id)
    if batch.processing_status != "ended":
        print("\nBatch hasn't finished yet - try again later.")
        return

    print("\nResults:\n")
    for result in client.messages.batches.results(batch_id):
        # Results can come back in any order; map custom_id back to the input text.
        index = int(result.custom_id.removeprefix("classify-"))
        if result.result.type == "succeeded":
            text = next(b.text for b in result.result.message.content if b.type == "text")
            print(f"  [{result.custom_id}] {text.strip():<10} {ITEMS[index]}")
        else:
            print(f"  [{result.custom_id}] {result.result.type:<10} {ITEMS[index]}")


def run():
    usage = "Usage: python main_submit_check_run.py submit | check [batch_id] | results [batch_id]"
    if len(sys.argv) < 2:
        print(usage)
        return

    command = sys.argv[1]
    client = anthropic.Anthropic()

    if command == "submit":
        submit(client)
        return

    if command not in ("check", "results"):
        print(usage)
        return

    if len(sys.argv) > 2:
        batch_id = sys.argv[2]
    elif BATCH_ID_FILE.exists():
        batch_id = BATCH_ID_FILE.read_text().strip()
    else:
        print("No batch ID given and no saved batch ID found - run 'submit' first.")
        return

    if command == "check":
        check(client, batch_id)
    else:
        results(client, batch_id)


if __name__ == "__main__":
    run()
