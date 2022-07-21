# ArchitectureLanguagePOC

JSON-based domain-specific language for describing MSA-based systems

Currently coupled with the diagrams Python library for generating a graphical model from the language

To setup, clone the repo, navigate to Diagrams/ and do ```pip install -r requirements.txt``` to get the Python project setup.

``node_types.json`` specifies the node types we used in the example pipelines. These node types, however, are not required and can be changed according to system requirements. The schema as well is highly extensible, and only requires a few standard things.