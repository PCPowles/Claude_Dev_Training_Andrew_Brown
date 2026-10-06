import time

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request


def run():
    client = anthropic.Anthropic()

    items = [
        "The product quality is excellent!",
        "Terrible customer service, never again.",
        "It's okay, nothing special.",
        "Absolutely love this, best purchase of the year.",
        "Shipping took forever and the box was damaged.",
        "This was best ever, return customer for sure!"
    ]

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
        for i, text in enumerate(items)
    ]

    batch = client.messages.batches.create(requests=requests)
    print(f"Submitted batch {batch.id} (status: {batch.processing_status})")

    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        counts = batch.request_counts
        total = counts.processing + counts.succeeded + counts.errored + counts.canceled + counts.expired
        print(f"  ...{batch.processing_status} ({counts.succeeded + counts.errored}/{total} done)")
        time.sleep(10)

    print(f"\nResults (succeeded: {batch.request_counts.succeeded}, "
          f"errored: {batch.request_counts.errored}):\n")

    for result in client.messages.batches.results(batch.id):
        if result.result.type == "succeeded":
            text = next(b.text for b in result.result.message.content if b.type == "text")
            print(f"  [{result.custom_id}] {text.strip()}")
        else:
            print(f"  [{result.custom_id}] {result.result.type}")


if __name__ == "__main__":
    run()
