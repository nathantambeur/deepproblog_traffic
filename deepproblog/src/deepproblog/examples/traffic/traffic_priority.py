import torch

from data import TrafficDataset, traffic_images
from deepproblog.dataset import DataLoader
from deepproblog.engines import ExactEngine
from deepproblog.model import Model
from deepproblog.network import Network
from deepproblog.train import train_model
from network import CNN3,CNN5
from torch.optim import Adam




directions = ["right", "down", "left", "up"]

networks= []
for dir  in directions:
    cnn = CNN5()
    net = Network(cnn, dir+"_net", batching=True)
    net.optimizer = torch.optim.Adam(cnn.parameters(), lr=1e-5)
    networks.append(net)

cnn = CNN3()
net = Network(cnn , "priority_net", batching=True)
net.optimizer = torch.optim.Adam(cnn.parameters(), lr=1e-5)
networks.append(net)

model = Model("priority_model.pl", networks)
model.set_engine(ExactEngine(model))

# print("traffic images", traffic_images.data)
model.add_tensor_source("traffic", traffic_images)
dataset = TrafficDataset()
print("dataset created" , dataset.to_queries())

query = dataset.to_query(0,1)
result = model.solve([query])[0]
print("result: ",result)
# Train the model
loader = DataLoader(dataset, 1, False)
train_model(model, loader, 1, log_iter=1, profile=0)



#model.save_state("snapshot/trained_model.pth")

# model.load_state("snapshot/trained_model.pth")
# Query the model
#query = dataset.to_query(0)
#result = model.solve([query])[0]
#print(result)
