import getpass
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from a .env file
load_dotenv()

# set the current module name to "big_sky"
# from organizer.agent_local import graph
from lang_memgpt import memgraph


# def _set_env(var: str):
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")


# _set_env("OPENAI_API_KEY")

config = {
    "configurable": {
        "model": "gpt-4o",
        "provider": "openai",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "qdrant_url": os.environ.get("QDRANT_URL"),
        "qdrant_api_key": os.environ.get("QDRANT_API_KEY"),
        "qdrant_collection_name": os.environ.get("QDRANT_COLLECTION_NAME"),
        "thread_id": "1",
        "user_id": "1",
    }
}

async def main():
    messages = []

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        async for event in memgraph.astream({"messages": messages}, config=config):
            for value in event.values():
                if value.get("messages") is None:
                    print("No messages", value)
                    continue

                # coerce a single message to an array
                if not isinstance(value["messages"], list):
                    value["messages"] = [value["messages"]]

                messages.extend(value["messages"])

                for message in value["messages"]:
                    if message.content:
                        print("Assistant:", message.content)
                    if hasattr(message, "tool_calls") and len(message.tool_calls) > 0:
                        print("Tool Calls", message.tool_calls)

if __name__ == "__main__":
    asyncio.run(main())