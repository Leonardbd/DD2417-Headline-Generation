from openai import OpenAI
from rouge_score import rouge_scorer
import difflib

client = OpenAI(api_key="sk-...")  #Your actual API key
fine_tuned_model = "ft:gpt-4.1-mini-2025-04-14:applitic::BbOtEzXA" #Your fine-tuned model ID
default_model = "gpt-4.1-mini-2025-04-14"

def ask_model(model_name, prompt):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Du är en assistent som hjälper till att skapa rubriker för nyhetsartiklar. Generera endast en rubrik."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def calculate_similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def calculate_rouge(predicted, ideal):
    rouge2 = rouge_scorer.RougeScorer(['rouge2'], use_stemmer=True)
    rouge3 = rouge_scorer.RougeScorer(['rouge3'], use_stemmer=True)

    r2_score = rouge2.score(ideal, predicted)['rouge2'].fmeasure
    r3_score = rouge3.score(ideal, predicted)['rouge3'].fmeasure

    return r2_score, r3_score

def main():
    input_text = input("Enter your article text:\n> ").strip()
    ground_truth = input("Enter expected/ground truth headline (or leave blank to skip):\n> ").strip()

    print("\n Querying models...")
    ft_output = ask_model(fine_tuned_model, input_text)
    default_output = ask_model(default_model, input_text)

    print("\n FINE-TUNED MODEL RESPONSE:\n", ft_output)
    print("\n DEFAULT MODEL RESPONSE:\n", default_output)

    if ground_truth:
        sim_ft = calculate_similarity(ft_output, ground_truth)
        sim_def = calculate_similarity(default_output, ground_truth)

        rouge2_ft, rouge3_ft = calculate_rouge(ft_output, ground_truth)
        rouge2_def, rouge3_def = calculate_rouge(default_output, ground_truth)

        print("\n EVALUATION METRICS")
        print("SequenceMatcher Similarity:")
        print(f"  Fine-tuned: {sim_ft:.2f}")
        print(f"  Default:    {sim_def:.2f}")

        print("\n ROUGE Scores:")
        print(f"  Fine-tuned ROUGE-2 F1: {rouge2_ft:.2%}")
        print(f"  Fine-tuned ROUGE-3 F1: {rouge3_ft:.2%}")
        print(f"  Default    ROUGE-2 F1: {rouge2_def:.2%}")
        print(f"  Default    ROUGE-3 F1: {rouge3_def:.2%}")

        # Exact match (case-insensitive)
        print("\n Exact Match:")
        print(f"  Fine-tuned: {ft_output.lower() == ground_truth.lower()}")
        print(f"  Default:    {default_output.lower() == ground_truth.lower()}")

if __name__ == "__main__":
    main()
