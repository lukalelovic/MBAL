from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

import json

# Open JSON file
f = open('../Extensions/exFullSystem.json')
data = json.load(f)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node with type
    def formatNode(node):
        if (node['nodeType'] == 'database'):
            return RDS(node['nodeName'])
        
        return EC2(node['nodeName'])


    # Fill node map with node ID as key, node name as value
    nodeMap = {}
    for node in nodes:
        nodeMap.update({ node['nodeID']: formatNode(node) })

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