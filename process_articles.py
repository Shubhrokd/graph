import os
from tqdm import tqdm
from connect import process_gpt4
from extract_text import extract_text_from_html
from preprocess import text_to_batches

base_path = "raw"
processed_articles = os.listdir("data")

for file_name in tqdm(os.listdir(base_path)):
    title = " ".join(file_name.split("_")[-1].split("-")[:-1])
    if f"results_{title}.txt" in processed_articles:
        continue

    results = ""
    with open(os.path.join(base_path, file_name), "r", encoding="utf-8") as f:
        content = f.read()
        extraction = extract_text_from_html(content)
        batches = text_to_batches(extraction)
        for batch in batches:
            gpt_results = process_gpt4(batch)
            results += gpt_results

    with open(f"data/results_{title}.txt", "w", encoding="utf-8") as results_file:
        results_file.write(results)

    with open(f"cleaned/cleaned_{title}.txt", "w", encoding="utf-8") as cleaned_file:
        cleaned_file.write(extraction)
