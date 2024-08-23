# Stu's Discord Bot

This is (or, will be, depending when you read this) a Discord bot that uses LangGraph to provide long-term memory to a Discord server.

It is based on the excellent [LangChain MemGPT](https://github.com/langchain-ai/lang-memgpt/) project, but unbroken to work with the latest LangGraph Studio.

Inspired by papers like [MemGPT](https://memgpt.ai/) and others.

![Process](./img/studio.gif)

The memory graph handles thread process deduplication and supports continuous updates to a single "memory schema" as well as "event-based" memories that can be queried semantically.

![Memory Diagram](./img/memory_graph.png)

#### Project Structure

```bash
├── langgraph.json # LangGraph Cloud Configuration
├── lang_memgpt
│   ├── __init__.py
│   └── graph.py # Define the agent w/ memory
├── poetry.lock
├── pyproject.toml # Project dependencies
└── tests # Add testing + evaluation logic
    └── evals
        └── test_memories.py
```

## Quickstart

### Prerequisites

This assumes a Mac with [Homebrew](https://brew.sh/) installed. Something similar is possible on Linux, but YMMV.

We need Poetry and Micromamba to install the dependencies and sandbox the environment.

```bash
brew install poetry micromamba
```

Then, install the dependencies:

```bash
poetry install
```

Create a [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) environment.

```bash
micromamba create python=3.10.13 -y -n stu-discord -c conda-forge
micromamba activate stu-discord
```

This example defaults to using Qdrant for its memory database, and OpenAI's `text-embedding-3-small` as the text encoder. For the LLM, we are using OpenAI's `gpt-4o`.

1. Visit [OpenAI](https://platform.openai.com/api-keys) to sign up and get an API Key
2. Visit [Qdrant Cloud](https://cloud.qdrant.io/) to create a server and get an API key. Also note your "Server URL". The free tier is fine for this example.
3. Visit [Tavily](https://app.tavily.com/) to get an API key.

Now set these values in the `.env` file. You can copy the contents of `.env.example` to get started.

```bash
TAVILY_API_KEY=...
OPENAI_API_KEY=...
QDRANT_API_KEY=...
QDRANT_URL=...
QDRANT_COLLECTION_NAME=stu-discord
```

### Running Locally

```bash
python ./local.py
```

Example session:

> *User*: Please remember that my anniversary is August 3rd, beginning in 2023
> No messages {'core_memories': ["The user's name is Daniel Walmsley."], 'recall_memories': []}
> *Tool Calls* [{'name': 'save_recall_memory', 'args': {'memory': "Daniel Walmsley's anniversary is August 3rd, starting in 2023."}, 'id': 'call_Bf8v2xdvsXkSxdvN9bPQJU64', 'type': 'tool_call'}]
> *Assistant*: Daniel Walmsley's anniversary is August 3rd, starting in 2023.
> *Assistant*: Got it! Your anniversary is on August 3rd, starting in 2023. If there's anything special you need help planning or remembering for next year's celebration, just let me know!

Then, in a different session, we can recall the memory:

> *User*: When is my anniversary?
> No messages {'core_memories': ["The user's name is Daniel Walmsley."], 'recall_memories': ["Daniel Walmsley's anniversary is August 3rd, starting in 2023."]}
> *Assistant*: Your anniversary is on August 3rd.

#### Deploy to LangGraph Cloud

**Note:** (_Closed Beta_) LangGraph Cloud is a managed service for deploying and hosting LangGraph applications. It is currently (as of 26 June, 2024) in closed beta. If you are interested in applying for access, please fill out [this form](https://www.langchain.com/langgraph-cloud-beta).

To deploy this example on LangGraph, fork this [repo](https://github.com/gravityrail/lang-memgpt).

Next, navigate to the 🚀 deployments tab on [LangSmith](https://smith.langchain.com/o/ebbaf2eb-769b-4505-aca2-d11de10372a4/).

**If you have not deployed to LangGraph Cloud before:** there will be a button that shows up saying `Import from GitHub`. You’ll need to follow that flow to connect LangGraph Cloud to GitHub.

Once you have set up your GitHub connection, select **+New Deployment**. Fill out the required information, including:

1. Your GitHub username (or organization) and the name of the repo you just forked.
2. You can leave the defaults for the config file (`langgraph.config`) and branch (`main`)
3. Environment variables (see below)

The default required environment variables can be found in [.env.example](.env.example) and are described in the previous section.

You can fill these out locally, copy the .env file contents, and paste them in the first `Name` argument.

Assuming you've followed the steps above, in just a couple of minutes, you should have a working memory service deployed!

Now let's try it out.

## Part 2: Setting up a Slack Bot

The langgraph cloud deployment exposes a general-purpose stateful agent via an API. You can connect to it from a notebook, UI, or even a Slack or Discord bot.

In this repo, we've included an `event_server` to listen in on Slack message events so you can talk with
your bot from slack.

The server is a simple [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) app that uses [Slack Bolt](https://slack.dev/bolt-python/tutorial/getting-started) to interact with Slack's API.

In the next step, we will show how to deploy this on GCP's Cloud Run.

#### How to deploy as a Discord bot


So now you've deployed the API, how do you turn this into an app?

Check out the [event server README](./event_server/README.md) for instructions on how to set up a Discord connector on Cloud Run.


## How to evaluate

Memory management can be challenging to get right. To make sure your schemas suit your applications' needs, we recommend starting from an evaluation set,
adding to it over time as you find and address common errors in your service.

We have provided a few example evaluation cases in [the test file here](./tests/evals/test_memories.py). As you can see, the metrics themselves don't have to be terribly complicated,
especially not at the outset.

We use [LangSmith's @test decorator](https://docs.smith.langchain.com/how_to_guides/evaluation/unit_testing#write-a-test) to sync all the evalutions to LangSmith so you can better optimize your system and identify the root cause of any issues that may arise.
