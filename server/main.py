import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.nn import BCEWithLogitsLoss
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from collections import defaultdict
import json

from output import log, init_log

from config import *


training_data = json.load(open("dataset.json", encoding="utf-8"))

init_log()

training_data = list({frozenset(d["text"]): d for d in training_data}.values())

all_unique_keys = sorted(list(set(key for item in training_data for key in item["labels"])))
key_to_id = {key: i for i, key in enumerate(all_unique_keys)}
id_to_key = {i: key for i, key in enumerate(all_unique_keys)}
num_labels = len(all_unique_keys)

log(f"Все уникальные ключи: {all_unique_keys}")
log(f"Количество уникальных ключей: {num_labels}\n")

class_counts = defaultdict(int)
for example in training_data: # Используем только обучающие данные для расчета весов
  for label in example['labels']:
    class_counts[label] += 1

# 2. Расчет весов, которые будут переданы в pos_weight для BCEWithLogitsLoss
# Веса должны быть в том же порядке, что и id_to_key
weights_tensor = torch.zeros(num_labels, dtype=torch.float)
total_train_samples = len(training_data)


log("Рассчитанные веса для каждого класса:")
for i in range(num_labels):
    label = id_to_key[i]
    count = class_counts.get(label, 0) # Количество положительных примеров для данного класса

    if count > 0:
        # Количество отрицательных примеров для данного класса
        # В многоместной классификации это не просто (total_samples - count)
        # Это скорее балансировка вклада True Positives vs False Positives
        # Более точная интерпретация: увеличение веса для positive examples,
        # чтобы модель уделяла им больше внимания, особенно если их мало.
        # Эта формула (N-P)/P часто используется и является одной из эвристик.
        num_negative_samples = total_train_samples - count
        weights_tensor[i] = num_negative_samples / count
    else:
        # Если класс отсутствует в обучающей выборке, его вес можно установить в 1.0 (нейтрально)
        # или в очень большое значение, если он должен быть важным, но отсутствует.
        # Для целей BCEWithLogitsLoss, 1.0 означает отсутствие специального взвешивания.
        weights_tensor[i] = 1.0
    log(f" {label}: {weights_tensor[i]:.4f} (встречается {count} раз)")

# 3. Вывод результатов
log("\nweights_tensor:", weights_tensor, "\n\n")
log("\nClass Counts:", class_counts,)


# --- 2. Подготовка данных для обучения ---

# Определяем токенизатор (модель для русского языка)
# 'DeepPavlov/rubert-base-cased' - это предобученная BERT-подобная модель для русского языка.
model_name = "DeepPavlov/rubert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Создаем пользовательский класс Dataset
class TextDataset(Dataset):
    def __init__(self, data, tokenizer, key_to_id, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.key_to_id = key_to_id
        self.max_len = max_len
        self.num_labels = len(key_to_id)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = str(item["text"])
        labels = item["labels"]

        # Токенизация текста
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding="max_length",
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        # Создание бинарного вектора для лейблов
        labels_vector = torch.zeros(self.num_labels, dtype=torch.float)
        for label in labels:
            if label in self.key_to_id:
                labels_vector[self.key_to_id[label]] = 1.0

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': labels_vector
        }

# Создаем экземпляры Dataset и DataLoader
train_dataset = TextDataset(training_data, tokenizer, key_to_id, MAX_LEN)
train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

val_dataset = TextDataset(validation_dataset, tokenizer, key_to_id, MAX_LEN)
val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False) # Не перемешиваем валидационный сет

# --- 3. Определение Модели ---

# Загружаем предобученную модель BERT для классификации
# problem_type="multi_label_classification" указывает, что это задача с несколькими метками
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels, problem_type="multi_label_classification")

# Определяем устройство (GPU если доступно, иначе CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- 4. Обучение Модели ---

# Оптимизатор
optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)

# Функция потерь для многоместной классификации (Binary Cross-Entropy with Logits)
# Logits - это сырые предсказания модели, без активации (например, Sigmoid).
# BCEWithLogitsLoss уже включает Sigmoid внутри себя для стабильности.
weights_tensor = weights_tensor.to(device)
loss_fn = BCEWithLogitsLoss(pos_weight=weights_tensor)

log(f"Начинаем обучение на устройстве: {device}\n")

model.train() # Переводим модель в режим обучения
for epoch in range(NUM_EPOCHS):
    total_loss = 0
    for batch_idx, batch in enumerate(train_dataloader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        optimizer.zero_grad() # Обнуляем градиенты перед новым проходом

        # Прямой проход
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits # Получаем сырые предсказания

        # Вычисляем потери
        loss = loss_fn(logits, labels)
        total_loss += loss.item()

        # Обратный проход и оптимизация
        loss.backward() # Вычисляем градиенты
        optimizer.step() # Обновляем веса модели

        if (batch_idx + 1) % 2 == 0: # Печатаем прогресс каждые 2 батча
            log(f" Эпоха {epoch+1}/{NUM_EPOCHS}, Батч {batch_idx+1}/{len(train_dataloader)}, Потеря: {loss.item():.4f}")

    avg_loss = total_loss / len(train_dataloader)
    log(f"Эпоха {epoch+1} завершена. Средняя потеря: {avg_loss:.4f}")


# model.eval() # Переводим модель в режим оценки
# total_val_loss = 0
# with torch.no_grad(): # Отключаем расчет градиентов
#     for batch_idx, batch in enumerate(val_dataloader):
#         input_ids = batch['input_ids'].to(device)
#         attention_mask = batch['attention_mask'].to(device)
#         labels = batch['labels'].to(device)

#         outputs = model(input_ids=input_ids, attention_mask=attention_mask)
#         logits = outputs.logits
#         loss = loss_fn(logits, labels)
#         total_val_loss += loss.item()

#     avg_val_loss = total_val_loss / len(val_dataloader)
#     log(f" Средняя потеря на валидации: {avg_val_loss:.4f}\n")


log("Обучение завершено.")

# --- 5. Использование обученной модели для предсказаний ---

model.eval() # Переводим модель в режим оценки (инференса)
log("\n--- Предсказания на новых запросах ---")

def predict_food_keys(text, model, tokenizer, id_to_key, key_to_id_map, max_len=MAX_LEN, threshold=0):
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


# Тестовые запросы
test_queries = [
    "Хочу что-то сладкое",
    "Ищу острое блюдо к ужину",
    "Что-нибудь прохладное попить",
    "Легкий салат на обед",
    "Хочу пиццу, но не острую",
    "Не знаю, что хочу, просто что-то для поднятия настроения",
    "Хочу пиццу",
    "Хочу что-то по типу шаурмы",
    "Хочу смузи с мороженным",
    "Хотелось бы попить пивка под футбол, что посоветуешь к пиву?",
    "Хочу пива холодного со стейком",
    "Хочу кфс",
    "Слушай, что ты можешь посоветовать человеку с язвой",
    "Я хочу что-нибудь со сливочным вкусом"
]

for query in test_queries:
    predicted_keys = predict_food_keys(query, model, tokenizer, id_to_key, key_to_id)

    log(f"\nЗапрос: '{query}'")

    log("\nПредсказанные ключи:", ", ".join([i["name"] for i in predicted_keys[:3]]))

    #Можно также вывести вероятности для каждого ключа, если нужно для отладки
    log("\nВероятности для всех ключей:")
    for item in predicted_keys:
        if(item["prob"] >= 0.5):
            log(item["name"] + ":", item["prob"])


output_dir = "./trained_model" # Папка, куда сохраняем модель
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
