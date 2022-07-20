from modulefinder import EXTENDED_ARG
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS

import json

# Open JSON file
f = open('../example.json')
data = json.load(f)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node with type
    def formatNode(node):
        if (node['nodeType'] == 'handler'):
            return Lambda(node['nodeName'])

        if (node['nodeType'] == 'storage'):
            return S3(node['nodeName'])

        if (node['nodeType'] == 'processor'):
            return SQS(node['nodeName'])

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
            depList >> Edge(minlen = "2", color = "black") >> nodeMap[node['nodeID']]
        else:
            nodeMap[node['nodeID']]

f.close()