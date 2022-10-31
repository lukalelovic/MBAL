# This file parses the train_ticket_new.json file into a new json file following our language's schema
# Better, faster, and more accurate than doing this manually.

import json

train_ticket = open('../train_ticket_new.json')
train_ticket_data = json.load(train_ticket)

nodes = []
nodeMap = {}

# Load the node service names into a map
for node in train_ticket_data['communication']['nodes']:
    nodeMap.update({ node['label']: {
        "nodeName": node['label'],
        "nodeType": "service",
        "nodeShape": node['shape'],
        "dependencies": [],
        "targets": []
    } })

# Populate the node map with the node's data
for edge in train_ticket_data['communication']['edges']:
    # Update source targets
    sourceName = edge['from']['label']
    targetName = edge['to']['label']

    def depOrTargetObj(nodeName):
        return {
            "nodeName": nodeName, 
            "requests": [edge['label']],
            "length": edge['length'],
            "width": edge['width']
        }
    
    # Append dependencies and targets
    nodeMap[targetName]['dependencies'].append(depOrTargetObj(sourceName))
    nodeMap[sourceName]['targets'].append(depOrTargetObj(targetName))

for node in nodeMap.values():
    nodes.append(node)

file = {
    "systemName": "train-ticket-system",
    "systemVersion": "0.2",
    "nodes": nodes
}

json_object = json.dumps(file, indent=4)

with open("example-trainticket.json", "w") as outfile:
    outfile.write(json_object)