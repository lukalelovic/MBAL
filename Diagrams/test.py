from diagrams import Diagram
from diagrams.aws.compute import EC2

import json

# Open JSON file
f = open('../Extensions/exFullSystem.json')
data = json.load(f)

nodes = data['nodes']

nodeMap = {}

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Fill node map with node ID as key, node name as value
    for node in nodes:
        nodeMap.update({ node['nodeID']: EC2(node['nodeName']) })

    # Iterate through all nodes
    for node in nodes:
        # Get node dependencies
        depLen = len(node['dependencies'])
        depList = []
        
        for i in range(depLen):
            depID = node['dependencies'][i]

            depList.append(nodeMap[depID])
        if len(depList) > 0:
            depList >> nodeMap[node['nodeID']]
        else:
            nodeMap[node['nodeID']]

f.close()