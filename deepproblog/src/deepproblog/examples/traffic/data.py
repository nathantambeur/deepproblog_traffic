import os
import pandas as pd
import ast
from PIL import Image
from pathlib import Path
from typing import List

import torchvision.transforms as transforms
from problog.logic import Term, Constant

from deepproblog.dataset import Dataset
from deepproblog.query import Query


transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)
root = Path(__file__).parent
class TrafficImages(object):
    def __init__(self, in_memory=True, transform=None):
        self.data = dict()
        self.image_root = root / "images" / "32images"
        self.in_memory = in_memory
        self.transform = transform
        if in_memory:
            for image in self.image_root.iterdir():
                name = self.image_root.name + "/" + image.name
                image = Image.open(image)
                if transform is not None:
                    image = transform(image)
                self.data[name] = image

    def get_image(self, path):
        if self.in_memory:
            return self.data[path]
        else:
            image = Image.open(self.image_root / path)
            if self.transform is not None:
                image = transform(image)
            return image
    def __getitem__(self, item):
        path = str(item[0].functor).strip('"')
        return self.get_image(path)

traffic_images = TrafficImages(True, transform)
path = os.path.dirname(os.path.abspath(__file__))

class TrafficDataset(Dataset):
    def __init__(
        self
    ):
        super().__init__()
        self.data = []
        df = pd.read_csv("~/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_scenarios.csv")
        
        df['prolog_priority'] = df['prolog_priority'].apply(lambda x: ast.literal_eval(x))
        self.data = list(df['prolog_priority'])
        
    def __len__(self):
        return len(self.data)
    
    def to_queries(self) -> List[Query]:
        """

        :return: A list of all queries in the dataset.
        """
        # ask a query about all directions right down left up
        return [self.to_query(i,0) for i in range(len(self))]+[self.to_query(i,1) for i in range(len(self))]+[self.to_query(i,2) for i in range(len(self))]+[self.to_query(i,3) for i in range(len(self))]

    def to_query(self, i,number):
        
        # ex [0,1,0,1] ==> right is 0, down is 1, left is 0, up is 1 ==> down and up get priority 
        answers = self.data[i] 
        
        path = "32images/img_" + str(i) + ".png"
       
        question = ["right", "down", "left", "up"][number]
        
        term = Term(question,Term("tensor", Term("traffic", Constant('"' + path + '"'))),Constant(int(answers[number])))
        
        return Query(term)
        
           
    def __len__(self):
        return len(self.data)
