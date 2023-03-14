import torch

from data import MNISTImages, AdditionDataset
from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model
from network import MNIST_Net

network = MNIST_Net()
net = Network(network, "mnist_net", batching=True)
net.optimizer = torch.optim.Adam(network.parameters(), lr=1e-3)

model = Model("addition.pl", [net])
model.set_engine(ExactEngine(model))
model.add_tensor_source("train", MNISTImages("train"))
model.add_tensor_source("test", MNISTImages("test"))

dataset = AdditionDataset("train")

# Train the model
loader = DataLoader(dataset, 32, True)
model.save_state("snapshot/trained_model.pth")

train_model(model, loader, 5, log_iter=1, profile=0)


# Query the model
query = dataset.to_query(0)
result = model.solve([query])[0]
print(result)
