from modulefinder import EXTENDED_ARG
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

import json

# Open JSON file
f = open('../example.json')
data = json.load(f)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node icon with type
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

        return EC2(node['nodeName'])

    def formatEdge(node, l, ndx):
        color = 'black'
        lbl = ''

        if 'previousSteps' in node and ndx < len(node['previousSteps']):
            lbl = node['previousSteps'][i]

        if 'requests' in node and ndx < len(node['requests']):
            requestType = node['requests'][ndx]

            if requestType == 'GET':
                color = 'green'
            elif requestType == 'POST' or requestType == 'PUT' or requestType == 'DELETE':
                color = 'red'
        
        return Edge(xlabel=lbl, minlen=l, color=color, fontsize="24")

    # Fill node map with node ID as key, node name as value
    nodeMap = {}
    for node in nodes:
        nodeMap.update({ node['nodeID']: formatNode(node) })

    # Iterate through all nodes
    for node in nodes:
        # Get node dependencies
        depLen = len(node['dependencies'])
        depList = []
        
        if depLen > 0:
            for i in range(depLen):
                depID = node['dependencies'][i]

                nodeMap[depID] >> formatEdge(node, "2", i) >> nodeMap[node['nodeID']]
        else:
            nodeMap[node['nodeID']]

f.close()