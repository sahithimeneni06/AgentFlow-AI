from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = 'google/flan-t5-base'

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def ask_llm(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=False
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)