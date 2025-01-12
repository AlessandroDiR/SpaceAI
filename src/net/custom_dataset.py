from torch import Tensor
from torch.utils.data import Dataset
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
import torchtext.transforms as T
import pandas as pd

class CustomDataset(Dataset):

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.tokenizer = get_tokenizer(tokenizer="spacy", language="it_core_news_sm")
        self.__build_vocab__()
    
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

        # 3. Trasformazione del testo di input
        transformed_input = self.__transform_input__(input_text)
        return transformed_input

    def __yield_tokens__(self):
        raw_inputs = self.data["Input"].to_list()
        for text in raw_inputs:
            yield self.tokenizer(text)
    
    def __build_vocab__(self):
        self.vocab = build_vocab_from_iterator(
            iterator=self.__yield_tokens__(),
            specials=["<unk>", "<pad>"],
            special_first=True
        )

    def __transform_input__(self, input) -> Tensor:
        tokens = self.tokenizer(input)
        transform_pipeline = T.Sequential(
            T.VocabTransform(self.vocab),
            T.ToTensor(padding_value=1))
        return transform_pipeline(tokens)

    def info(self):
        print("Dataset Info")
        print("---------------------------------")
        print(f"Data location:\t\"{self.file_path}\"")
        print(f"Data length:\t{len(self.data)} records")
        print(f"Vocab length:\t{len(self.vocab)} words")
        print("---------------------------------")

if __name__ == "__main__":
    cd = CustomDataset(file_path="../data/datasets/train/train.csv")
    cd.info()

    for i, cd in enumerate(cd):
        if i > 5: break
        print(f"Campione {i}: {cd}")
