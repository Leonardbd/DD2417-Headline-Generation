from openai import OpenAI
import difflib


client = OpenAI(api_key="sk-...") #Your API key here

fine_tuned_model = "ft:..." #Id of your finetuned model here
default_model = "gpt-4.1-mini-2025-04-14"

def ask_model(model_name, prompt):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Du är en assistent som hjälper till att skapa rubriker för nyhetsartiklar."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def calculate_similarity(prediction, ground_truth):
    seq_matcher = difflib.SequenceMatcher(None, prediction, ground_truth)
    return seq_matcher.ratio()

def main():

    input_text = input("Enter your text prompt: ").strip()

    ground_truth = input("Enter expected/ground truth answer (or leave blank to skip): ").strip()


    fine_tuned_response = ask_model(fine_tuned_model, input_text)
    default_response = ask_model(default_model, input_text)


    print("\nFINE-TUNED MODEL RESPONSE:\n", fine_tuned_response)
    print("\nDEFAULT MODEL RESPONSE:\n", default_response)

    if ground_truth:
        ft_similarity = calculate_similarity(fine_tuned_response, ground_truth)
        default_similarity = calculate_similarity(default_response, ground_truth)

        print("\n🔍 ACCURACY METRICS (similarity to ground truth):")
        print(f"Fine-tuned model similarity: {ft_similarity:.2f}")
        print(f"Default model similarity:   {default_similarity:.2f}")

        # Optional: Exact match
        ft_exact = fine_tuned_response.lower() == ground_truth.lower()
        default_exact = default_response.lower() == ground_truth.lower()
        print(f"\nExact match (fine-tuned): {ft_exact}")
        print(f"Exact match (default):    {default_exact}")

if __name__ == "__main__":
    main()
