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
    # cnn.load_state_dict(torch.load('model_classification_tutorial_'+dir+'.pt'))
    net = Network(cnn, dir+"_net", batching=True)
    net.optimizer = torch.optim.Adam(cnn.parameters(), lr=1e-3)
    networks.append(net)

cnn = CNN3()
# cnn.load_state_dict(torch.load('model_classification_tutorial_prio.pt'))
net = Network(cnn , "priority_net", batching=True)
net.optimizer = torch.optim.Adam(cnn.parameters(), lr=1e-3)
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
model.load_state("snapshot/trained_model_4.pth")
loader = DataLoader(dataset, 32, True)
for i in range(200):
    # model.save_state("snapshot/trained_model_"+str(i)+".pth")

    train_model(model, loader, 1, log_iter=1, profile=0)


