from modulefinder import EXTENDED_ARG
from turtle import color
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.analytics import DataPipeline
from diagrams.aws.general import GenericDatabase, User
from diagrams.aws.network import APIGateway, APIGatewayEndpoint
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.enablement import ManagedServices, ProfessionalServices
from diagrams.aws.storage import S3GlacierArchive
from diagrams.aws.management import Config, ManagedServices as MS
from diagrams.custom import Custom

import json

# Open JSON file
f = open('../Extensions/exFullSystem.json')
data = json.load(f)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node with type
    def formatNode(node):
        if (node['nodeType'] == 'pipeline'): return DataPipeline(node['nodeName'])
        elif (node['nodeType'] == 'database'): return GenericDatabase(node['nodeName'])
        elif (node['nodeType'] == 'proxy'): return APIGateway(node['nodeName'])
        elif (node['nodeType'] == 'service'): return ManagedServices(node['nodeName'])
        elif (node['nodeType'] == 'bucket'): return SimpleStorageServiceS3Bucket(node['nodeName'])
        elif (node['nodeType'] == 'kafka'): return ManagedStreamingForKafka(node['nodeName'], color = "black")
        elif (node['nodeType'] == 'config'): return Config(node['nodeName'])
        elif (node['nodeType'] == 'API'): return APIGatewayEndpoint(node['nodeName'])
        elif (node['nodeType'] == 'writer'): return MS(node['nodeName'])
        elif (node['nodeType'] == 'customer'): return ProfessionalServices(node['nodeName'])
        elif (node['nodeType'] == 'archive'): return S3GlacierArchive(node['nodeName'])
        elif (node['nodeType'] == 'srcSink'): return User(node['nodeName'])
        elif (node['nodeType'] == 'layer'): return Custom(node['nodeName'], "./custom_white_box.png")

        return EC2(node['nodeName'])

    def formatEdge(node, l):
        color = 'black'

        if (node['nodeType'] == 'API'):
            color = 'green'
        
        return Edge(minlen=l, color=color)


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
            depList >> formatEdge(node, "2") >> nodeMap[node['nodeID']]
        else:
            nodeMap[node['nodeID']]

f.close()