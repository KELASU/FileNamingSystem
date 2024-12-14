import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from sklearn.metrics import accuracy_score
import torch.nn as nn

data = pd.read_csv("path/to/your/file.csv")

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

data["text"] = data["text"].apply(lambda x: tokenizer.encode(x, max_length=512, truncation=True))

class CustomDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __getitem__(self, idx):
        sample = self.data.iloc[idx]
        inputs = self.tokenizer.encode_plus(
            sample["text"],
            add_special_tokens=True,
            max_length=512,
            return_attention_mask=True,
            return_tensors="pt",
        )
        labels = {
            "name": sample["name"],
            "id": sample["id"],
            "date": sample["date"],
            "title": sample["title"],
        }
        return {
            "input_ids": inputs["input_ids"].flatten(),
            "attention_mask": inputs["attention_mask"].flatten(),
            "labels": labels,
        }

    def __len__(self):
        return len(self.data)

dataset = CustomDataset(data, tokenizer)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=4)

class CustomLoss(nn.Module):
    def __init__(self):
        super(CustomLoss, self).__init__()
        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, outputs, labels):
        name_loss = self.loss_fn(outputs[:, 0], labels["name"])
        id_loss = self.loss_fn(outputs[:, 1], labels["id"])
        date_loss = self.loss_fn(outputs[:, 2], labels["date"])
        title_loss = self.loss_fn(outputs[:, 3], labels["title"])
        return name_loss + id_loss + date_loss + title_loss

optimizer = AdamW(model.parameters(), lr=1e-5)
loss_fn = CustomLoss()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in train_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"]
        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=attention_mask)
        loss = loss_fn(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss / len(train_loader)}")

    model.eval()
    total_correct = 0
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"]
            outputs = model(input_ids, attention_mask=attention_mask)
            _, predicted = torch.max(outputs.logits, dim=1)
            total_correct += (predicted == labels["name"]).sum().item()
    accuracy = total_correct / len(val_dataset)
    print(f"Validation accuracy: {accuracy:.4f}")

model.save_pretrained("path/to/save/")