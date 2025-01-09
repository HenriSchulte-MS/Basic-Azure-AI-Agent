import os
import argparse
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def main():
    parser = argparse.ArgumentParser(description='Delete an agent by ID.')
    parser.add_argument('agent_id', type=str, help='The ID of the agent to delete')
    args = parser.parse_args()

    agent_id = args.agent_id
    # Use agent_id in your code
    print(f'Deleting agent with ID: {agent_id}')
    # agent.id = agent_id  # Assuming you need to set agent.id somewhere

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )

    project_client.agents.delete_agent(agent_id)
    print("Deleted agent")

if __name__ == '__main__':
    main()