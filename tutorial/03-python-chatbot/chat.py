from langchain.llms.llamacpp import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import chainlit as cl
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider


# definition of llama.cpp engine
MODEL_PATH = "/home/pali/workspace/data/models/openchat_3.5.Q5_K_M.gguf"

@cl.cache
def instantiate_llm():
    # See the params explanation here: https://llama-cpp-python.readthedocs.io/en/latest/api-reference/
    llm = LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=1024,
        temperature=1,
        max_tokens=500,
        verbose=True,  # Verbose is required to pass to the callback manager
        streaming=True,
    )
    return llm


llm = instantiate_llm()

# helper function from chainlit playground to auto create llm provider
add_llm_provider(
    LangchainGenericProvider(id=llm._llm_type, name="Llama-cpp", llm=llm, is_chat=False)
)

# chainlit method called when the application starts
@cl.on_chat_start
def main():
    template = """### System Prompt
The following is a friendly conversation between a human and an AI in a style of Dungeons and dragons text games. The AI provides narrator context in a style of non playable characters. The AI answers in complete sentences up to 500 tokens:

### Current conversation:
{history}

### User Message
{input}

### Assistant"""

    prompt = PromptTemplate(template=template, input_variables=["history", "input"])

    conversation = ConversationChain(
        prompt=prompt, llm=llm, memory=ConversationBufferWindowMemory(k=10)
    )

    cl.user_session.set("conv_chain", conversation)

# chainlit method called every time user sends a message
@cl.on_message
async def main(message: cl.Message):
    conversation = cl.user_session.get("conv_chain")

    cb = cl.LangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["Assistant"]
    )

    cb.answer_reached = True

    res = await cl.make_async(conversation)(message.content, callbacks=[cb])