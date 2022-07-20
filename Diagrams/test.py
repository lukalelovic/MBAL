from modulefinder import EXTENDED_ARG
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import DataPipeline
from diagrams.aws.general import GenericDatabase, InternetGateway, User, Toolkit
from diagrams.aws.network import APIGateway, APIGatewayEndpoint
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.enablement import ManagedServices, ProfessionalServices
from diagrams.aws.storage import S3GlacierArchive
from diagrams.aws.management import Config, ManagedServices as MS

import json

# Open JSON file
f = open('../Extensions/exFullSystem.json')
data = json.load(f)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node with type
    def formatNode(node):
        if (node['nodeType'] == 'pipeline'):
            return DataPipeline(node['nodeName'])

        if (node['nodeType'] == 'database'):
            return GenericDatabase(node['nodeName'])

        if (node['nodeType'] == 'proxy'):
            return APIGateway(node['nodeName'])

        if (node['nodeType'] == 'service'):
            return ManagedServices(node['nodeName'])   
            
        if (node['nodeType'] == 'bucket'):
            return SimpleStorageServiceS3Bucket(node['nodeName'])    

        if (node['nodeType'] == 'kafka'):
            return ManagedStreamingForKafka(node['nodeName'], color = "black")   

        if (node['nodeType'] == 'config'):
            return Config(node['nodeName'])   

        if (node['nodeType'] == 'API'):
            return APIGatewayEndpoint(node['nodeName'])        
            
        if (node['nodeType'] == 'writer'):
            return MS(node['nodeName'])
            
        if (node['nodeType'] == 'customer'):
            return ProfessionalServices(node['nodeName'])                                      

        if (node['nodeType'] == 'archive'):
            return S3GlacierArchive(node['nodeName'])

        if (node['nodeType'] == 'srcSink'):
            return User(node['nodeName'])    

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