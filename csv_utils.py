import os
import csv


def save_to_csv(filename: str, transcript: str, summary: str, sentiment: str):
    file_exists = os.path.exists(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Transcript", "Summary", "Sentiment"])
        writer.writerow([transcript, summary, sentiment])
