from modulefinder import EXTENDED_ARG
from diagrams import Diagram, Edge, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.analytics import DataPipeline
from diagrams.aws.general import GenericDatabase, User
from diagrams.aws.network import APIGateway, APIGatewayEndpoint
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.enablement import ManagedServices, ProfessionalServices
from diagrams.aws.storage import S3GlacierArchive
from diagrams.aws.management import Config, ManagedServices as MS
from diagrams.generic.blank import Blank

import json
from jsonschema import validate

# Open JSON example file
example = open('../Examples/example-redhat2.json')
data = json.load(example)
example.close()

# Open JSON schema file
schema_file = open('../schema.json')
schema = json.load(schema_file)
schema_file.close()

# Validate the example follows the schema (or throw exception)
validate(instance=data, schema=schema)

nodes = data['nodes']

# Generate diagram based on node map
with Diagram(data['systemName'] + '-' + data['systemVersion']):
    # Format node icon with type
    def formatNode(node):
        if node['nodeType'] == 'pipeline': return DataPipeline(node['nodeName'])
        elif node['nodeType'] == 'database': return GenericDatabase(node['nodeName'])
        elif node['nodeType'] == 'proxy': return APIGateway(node['nodeName'])
        elif node['nodeType'] == 'service': return ManagedServices(node['nodeName'])
        elif node['nodeType'] == 'bucket': return SimpleStorageServiceS3Bucket(node['nodeName'])
        elif node['nodeType'] == 'kafka': return ManagedStreamingForKafka(node['nodeName'], color = "black")
        elif node['nodeType'] == 'config': return Config(node['nodeName'])
        elif node['nodeType'] == 'API': return APIGatewayEndpoint(node['nodeName'])
        elif node['nodeType'] == 'writer': return MS(node['nodeName'])
        elif node['nodeType'] == 'customer': return ProfessionalServices(node['nodeName'])
        elif node['nodeType'] == 'archive': return S3GlacierArchive(node['nodeName'])
        elif node['nodeType'] == 'srcSink': return User(node['nodeName'])
        elif node['nodeType'] == 'cluster': return Blank(node['nodeName'])
        
        # Create clusters
        with Cluster("Source/Sink Cluster"):
            ss_primary - ["Customer-cluster"]

        return EC2(node['nodeName'])

    def formatEdge(dependency):
        color = 'black'
        lbl = ''

        if 'requests' in dependency:
            # Get only the first request step and color
            mainRequest = dependency['requests'][0]
            lbl = mainRequest['executionStep']

            reqType = mainRequest['requestType']

            if reqType == 'GET':
                color = 'green'
            elif reqType == 'POST' or reqType == 'DELETE':
                color = 'red'
            elif reqType == 'PUT':
                color = 'blue'
        
        return Edge(xlabel=lbl, minlen="2", color=color, fontsize="24")

    # Fill node map with node ID as key, node name as value
    nodeMap = {}
    for node in nodes:
        nodeMap.update({ node['nodeName']: formatNode(node) })

    # Iterate through all nodes
    for node in nodes:
        # Get node dependencies
        depLen = len(node['dependencies'])
        depList = []
        nodeType = node['nodeType']

        if depLen > 0:
            for i in range(depLen):
                dep = node['dependencies'][i]
                depName = dep['nodeName']
                
                nodeMap[depName] >> formatEdge(dep) >> nodeMap[node['nodeName']]
        else:
            nodeMap[node['nodeName']]
    
