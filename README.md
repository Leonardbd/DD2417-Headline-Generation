# DD2417-Headline-Generation
This is a small project for the KTH course DD2417 Language Engineering. It fine-tunes the model gpt-4.1-mini-2025-04-14 to optimize it for generating headlines for Swedish news articles.

To install the necessary modules, run:
pip install -r requirements.txt

## Preprocessing
The final data for training, validation, and testing can be found in the "data" folder. If you want to jump straight to training, you can skip this step. However, if you’d like to preprocess the ClefKorpus dataset yourself, run the script process_data.py and split it into training, validation, and testing sets as needed.

## Training
Run train.py. This script performs a grid search over the hyperparameters described in the report.
Important: Enter your own OpenAI API key in the script. After training, the script will print the model_id (e.g., ft:gpt-4.1-mini-2025-04-14...). Save this model_id for use in program.py and run_eval.py.

## Evaluation
Run run_eval.py, and enter your OpenAI API key and model_id. This script evaluates the model’s performance using the following metrics:
- Exact matches
- Test accuracy
- Average similarity
- Average ROUGE-2 score
- Average ROUGE-3 score

You can find the training and validation loss curves in your OpenAI dashboard.

## Program
Run program.py, and enter your OpenAI API key and model_id. This script takes an article and its reference (ground-truth) headline as input, and then compares the generated headline from your fine-tuned model to the default GPT-4.1 output.
