# This file parses the train_ticket_new.json file into a new json file following our language's schema
# Better, faster, and more accurate than doing this manually.

import json

train_ticket = open('../train_ticket_new.json')
train_ticket_data = json.load(train_ticket)

nodes = []
nodeMap = {}

# Load the node service names into a map
for node in train_ticket_data['nodes']:
    nodeMap.update({ node['id']: {
        "nodeName": node['id'],
        "nodeType": "service",
        "dependencies": [],
        "targets": []
    } })

# Populate the node map with the node's data
for link in train_ticket_data['links']:
    # Update source targets
    sourceName = link['source']
    targetName = link['target']

    requests = []
    for function in link['functions']:
        requests.append(function)

    def depOrTargetObj(nodeName):
        return {
            "nodeName": nodeName, 
            "requests": link['functions'],
            "strength": link['strength']
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