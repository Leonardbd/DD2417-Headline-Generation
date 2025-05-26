import openai
import json
from difflib import SequenceMatcher
from rouge_score import rouge_scorer
import statistics


client = openai.OpenAI(api_key="sk-...")  #Replace with your actual key


model_id = "ft:..." #Replace with your trained model id


with open("data\\test.jsonl", "r", encoding="utf-8") as f:
    eval_data = [json.loads(line) for line in f]


exact_matches = 0
similarities = []

rouge2_scorer = rouge_scorer.RougeScorer(['rouge2'], use_stemmer=True) #Bigram
rouge3_scorer = rouge_scorer.RougeScorer(['rouge3'], use_stemmer=True) #Trigram

rouge2_scores = []  
rouge3_scores = []  

for i, item in enumerate(eval_data):
    prompt = item["input"]
    ideal = item["ideal"]

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "Du är en assistent som hjälper till att skapa rubriker för nyhetsartiklar."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        predicted = response.choices[0].message.content.strip()

        is_exact = predicted.upper() == ideal.upper()
        if is_exact:
            exact_matches += 1

        similarity = SequenceMatcher(None, predicted.lower(), ideal.lower()).ratio()
        similarities.append(similarity)

        #Compute ROUGE-2 and ROUGE-3
        r2 = rouge2_scorer.score(ideal, predicted)['rouge2'].fmeasure
        r3 = rouge3_scorer.score(ideal, predicted)['rouge3'].fmeasure
        rouge2_scores.append(r2)
        rouge3_scores.append(r3)

        print(f"\nExample {i + 1}")
        print(f"Prompt: {prompt[:60]}...")
        print(f"Ideal: {ideal}")
        print(f"Predicted: {predicted}")
        print(f"Exact match: {is_exact}")
        print(f"Similarity: {similarity:.2f}")
        print(f"ROUGE-2 F1: {r2:.2%} | ROUGE-3 F1: {r3:.2%}")
        print("-" * 50)

    except Exception as e:
        print(f"\n[!] Error on example {i + 1}: {e}")

print("\n=== Evaluation Summary ===")
print(f"Total examples: {len(eval_data)}")
print(f"Exact matches: {exact_matches}")
print(f"Accuracy: {exact_matches / len(eval_data):.2%}")
if similarities:
    print(f"Average similarity: {sum(similarities) / len(similarities):.2%}")
else:
    print("Average similarity: N/A (no successful outputs)")
print(f"Average ROUGE-2 F1: {statistics.mean(rouge2_scores):.2%}")
print(f"Average ROUGE-3 F1: {statistics.mean(rouge3_scores):.2%}")