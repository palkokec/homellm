![chatbot](./example.png)
In this example we are building simple chatbot based on python langchain, llamacpp and chainlit.
Chainlit provides ChatGPT like web user interface to interact with LLM.

# Code process flow
```
/*
+--------------------+
|Initialize LLM with |
|llama.cpp python    |
| +----------------+ |
| | choose model   | |
| +----------------+ |
| +----------------+ |
| | finetune with  | |
| | temperature    | | 
| | top_p and top_k| |
| +----------------+ |
+-----------+--------+
            |
            |
+--------------------+
| Add LLM provider   |
+-----------+--------+
            |
            |
+---------------------+
| on_chat_start       |
|                     |
| called once on app  |
| start               |
|                     |
| +-----------------+ |
| | create session  | |
| +-----------------+ |
| +-----------------+ |
| | create prompt   | |
| | and conversation| | 
| | chain           | |
| +-----------------+ |
+-----------+---------+
            |
            |
+---------------------+
| on_message          |
|                     |
| called every time   |
| message recieved    |
|                     |
| +-----------------+ |
| | load session    | |
| +-----------------+ |
| +-----------------+ |
| | async process   | |
| | message by llm  | | 
| | within context  | |
| +-----------------+ |
+-----------+---------+
 */
 ```
 
# Deployment Steps

Create virtual python environment in current folder (.) or specify directory name instead of .

```
python3 -m venv .
```

Initialize the virtual environment

```
source ./bin/activate
```

Install required python modules

```
python3 -m pip install -r requirements.txt
```

Run the chatbot

```
chainlit run chat.py -w --port 9999
```