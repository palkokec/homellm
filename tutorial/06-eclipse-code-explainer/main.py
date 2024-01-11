from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
import sys

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="/home/pali/workspace/data/models/codeninja-1.0-openchat-7b.Q5_K_S.gguf",
    temperature=0.75,
    max_tokens=2000,
    n_ctx=4096,
    top_p=1,
    callback_manager=callback_manager,
    verbose=False,  # Verbose is required to pass to the callback manager
)

with open(sys.argv[1]) as f:
    data = f.read()
    prompt = f"""Summarize, provide explanation and comment out the following java code: {data}"""
    llm(prompt)