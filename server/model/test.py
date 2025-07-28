import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json


training_data = json.load(open("../model/dataset.json", encoding="utf-8"))

training_data = list({frozenset(d["text"]): d for d in training_data}.values())

all_unique_keys = sorted(list(set(key for item in training_data for key in item["labels"])))
key_to_id = {key: i for i, key in enumerate(all_unique_keys)}
id_to_key = {i: key for i, key in enumerate(all_unique_keys)}

model_name = "../trained_model"
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForSequenceClassification.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def predict_food_keys(text, model, tokenizer, id_to_key, key_to_id_map, max_len=128, threshold=0):
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=max_len,
        return_token_type_ids=False,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    with torch.no_grad(): # Отключаем расчет градиентов для предсказания
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits # Получаем сырые предсказания

    # Применяем сигмоиду, чтобы получить вероятности (от 0 до 1)
    probabilities = torch.sigmoid(logits)

    # Выбираем ключи, вероятность которых выше порога
    predicted_labels_indices = (probabilities > threshold).nonzero(as_tuple=True)[1].tolist()

    # Преобразуем индексы обратно в строковые ключи
    predicted_keys = [id_to_key[idx] for idx in predicted_labels_indices]


    probs = probabilities.squeeze().tolist()

    predicted_keys = [{"name": id_to_key[idx], "prob": probs[idx]} for idx in predicted_labels_indices]
    predicted_keys = sorted(predicted_keys, key=lambda k: k["prob"], reverse=True)

    return predicted_keys


def get_keys(query):
    predicted_keys = predict_food_keys(query, model, tokenizer, id_to_key, key_to_id)

    keys = [i["name"] for i in predicted_keys[:3]]
    return keys