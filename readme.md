# Basic AI Agent with Azure AI Agent Service

This repo contains a simple example of a command-line AI agent utilizing Azure AI Agent Service. 

To run this sample:
1. Follow the [setup instructions in the docs](https://learn.microsoft.com/en-us/azure/ai-services/agents/quickstart?pivots=programming-language-python-azure). The basic agent setup is sufficient for this example.
1. Clone this repo and install the requirements, e.g., using ```pip install -r requirements.txt```.
1. Rename ```.env.example``` to ```.env``` and add the connection string of your AI Foundry project.
1. Ensure that you can authenticate using [Azure Default Credential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python), e.g., by logging into your Azure CLI (```az login```).
1. Optional: Review the ```get_sales_data``` function and modify it or add your own custom functions for the assistant to call.
1. Run ```basic_ai_agent.py```. The assistant can call the custom functions as well as write and execute Python code on the fly (Code Interpreter). Try asking "Please give me a bar chart of the sales data for 2024".