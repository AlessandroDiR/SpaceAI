from torch.utils.data import Dataset
from torchtext.data.utils import get_tokenizer
from pathlib import Path
import pandas as pd

class CustomDataset(Dataset):
    data: pd.DataFrame

    def __init__(self, root: str):
        self.data = pd.read_csv(root)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        # 1. Leggo la riga
        row = self.data.iloc[index]

        # 2. Separo le informazioni della riga
        input_text = row["Input"]
        action = row["Action"]
        asset = row["Asset"]
        start = row["Start"]
        end = row["End"]

        # 3. Pre-processing dell'input
        tokens = self.__tokenize__(input_text)

        # 4. Pre-processing dei target
        return {"input": tokens, "action": action, "asset": asset, "start": start, "end": end}
    
    def __tokenize__(self, text):
        tokenizer = get_tokenizer("spacy", language="it_core_news_sm")
        return tokenizer(text)
    

if __name__ == "__main__":
    cd = CustomDataset(root="../data/datasets/train/train.csv")

    for i, data in enumerate(cd):
        if i == 5:
            break
        print(f"Campione {i}, Data: {data}")
