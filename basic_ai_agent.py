import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, ToolSet, CodeInterpreterTool
import logging
import random
import json
from dotenv import load_dotenv


# Custom functions that the assistant can call


def get_sales_data(year: int):
    """
    Get product sales data for a given year.

    :param year (int): The year for which to get the sales data.
    :return: A JSON string containing sales data.
    :rtype: str
    """
    logging.info(f"Getting sales data for year: {year}")
    mock_data = []
    for i in range(10):  # Generate 10 mock sales records
        record = {
            'id': i + 1,
            'product': f'Product {i + 1}',
            'quantity_sold': random.randint(1, 100),
            'cost_price': round(random.uniform(5.0, 50.0), 2),
            'selling_price': round(random.uniform(10.0, 100.0), 2),
            'profit': lambda cp, sp, qty: round((sp - cp) * qty, 2)
        }
        record['profit'] = record['profit'](record['cost_price'], record['selling_price'], record['quantity_sold'])
        mock_data.append(record)
    return json.dumps(mock_data)


# End of custom functions


def main():

    # Define a directory to save files
    FILES_DIR = "files"
    os.makedirs(FILES_DIR, exist_ok=True)

    # Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
    # It should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"

    project_client = AIProjectClient.from_connection_string(
        credential=DefaultAzureCredential(),
        conn_str=os.environ["PROJECT_CONNECTION_STRING"],
    )

    # Initialize agent toolset with user functions and code interpreter
    functions = FunctionTool([
        get_sales_data,
        # Add additional functions here
    ])
    toolset = ToolSet()
    toolset.add(functions)
    toolset.add(CodeInterpreterTool())

    # Create agent with toolset and process a run

    agent = project_client.agents.create_agent(
        model="gpt-4o-mini", name="my-agent", instructions="You are a helpful agent", toolset=toolset
    )
    logging.info(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    logging.info(f"Created thread, ID: {thread.id}")

    # Chat loop
    print("Chat with the agent. Type 'exit' to quit.")
    while True:

        try:

            # Get user input
            user_input = input("User: ")
            if user_input == "exit":
                break

            # Create message to thread
            message = project_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input,
            )
            logging.info(f"Created message, ID: {message.id}")

            # Create and process agent run in thread with tools
            run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
            logging.info(f"Run finished with status: {run.status}")

            if run.status == "failed":
                logging.error(f"Run failed: {run.last_error}")
                break

            # Fetch and log last message
            messages = project_client.agents.list_messages(thread_id=thread.id)
            response_msg = messages.get_last_message_by_sender("assistant")
            for text_msg in response_msg.text_messages:
                print(f"Assistant: {text_msg.text.value}")

            # Save and open image if available
            for image_content in response_msg.image_contents:
                logging.info(f"Image File ID: {image_content.image_file.file_id}")
                file_name = f"{image_content.image_file.file_id}_image_file.png"
                file_path = os.path.join(FILES_DIR, file_name)
                project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name, target_dir=FILES_DIR)
                logging.info(f"Saved image file to: {file_path}")
                os.startfile(file_path)  # Open the saved image file

        except Exception as e:
            logging.error(f"An error occurred: {e}")

    # Delete the agent when done
    project_client.agents.delete_agent(agent.id)
    logging.info("Deleted agent")


if __name__ == "__main__":
    load_dotenv() # Load environment variables from .env file
    main()