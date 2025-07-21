https://onemain.atlassian.net/browse/ACQE-309

Notes in progress

Vanna.ai

What is it?

http://Vanna.ai  is a tool to generate SQL queries based on natural language. It can be setup completely locally, meaning it's safe to use with our database schema. I tested it locally using. The configuration we're currently using is Ollama, ChromaDB, and PostgreSQL.

Findings

Out of the box there isn't enough context to generate useful queries without a lot of hand holding. The results will only be as good as the training data. The types and advice are outlined here https://vanna.ai/docs/training-advice/.

Limitations

The quality of results are of course limited by the quality of the training data. In order for it to keep adding to the corpus of training data we’d really need someone who essentially already knows the answers to the queries.

This app will just make up tables and columns that don’t exist. The SQL can be manually corrected, but knowledge of the system is required.

From the initial research, it don’t look like we’d be able to connect to multiple DBs, so no Frontend if we’re training on Acquisition.

Things to Look into

It doesn't look like it's possible to connect to multiple DBs. We need Frontend as well as Acquisition.

Can we get a list of top queries? If so we can iterate through them and maybe add more context.

Setup

Create and navigate to a new directory for containing any vanna.ai related files,

mkdir ~/omf/springleaf/vanna_ai
cd ~/omf/springleaf/vanna_ai

Install Python 3.11.13

This version is needed in order to run Vanna.ai

asdf plugin add python
asdf install python 3.11.13
asdf set -u python 3.11.13

Install Ollama

brew install ollama

In order to run Vanna.ai you'll need to have the ollama server running.

ollama serve

Optional (Strictly for Fun)

Running the ollama console has no bearing on vana.ai!
This is strictly for if you want to play around with the LLM locally.

If you want interact with ollama directly from the terminal, simply choose a llama to download and use. Be sure to make sure your system can handle the one you choose! There's more information here on the individual models.

Mac's Memory

Model Suggestion

16 GB

llama3.2:1b

24 GB

llama3.2:3b

32 GB

llama3.2-vision

64 GB

llama3.3

To get to its console, run this command. Whatever llama version you enter will be downloaded and used.

 ollama run llama3.2-vision

Install http://Vanna.ai

pip install 'vanna[chromadb,ollama,postgres]'

To initially set the training data, run TRAIN_MODEL=true python vanna_ai.py.

To run the server use python vanna_ai.py.

To retrain run RETRAIN_MODEL=true python vanna_ai.py

Once it's started, navigate to http://localhost:8084/#
From here you'll be able to start playing around with it.