import os
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import (
    ConversationalRetrievalChain,
)

from langchain.docstore.document import Document
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider

import chainlit as cl

# definition of llama.cpp engine
MODEL_PATH = "/home/pali/workspace/data/models/openchat_3.5.Q5_K_M.gguf"

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

@cl.cache
def instantiate_llm():
    # See the params explanation here: https://llama-cpp-python.readthedocs.io/en/latest/api-reference/
    llm = LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=1024,
        temperature=1,
        max_tokens=200,
        verbose=True,  # Verbose is required to pass to the callback manager
        streaming=True,
    )
    return llm


llm = instantiate_llm()

# helper function from chainlit playground to auto create llm provider
add_llm_provider(
    LangchainGenericProvider(id=llm._llm_type, name="Llama-cpp", llm=llm, is_chat=False)
)

@cl.on_chat_start
async def on_chat_start():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!",
            accept=["text/plain"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...", disable_feedback=True)
    await msg.send()

    with open(file.path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split the text into chunks
    texts = text_splitter.split_text(text)

    # Create a metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # Create a Chroma vector store
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embedding_function, metadatas=metadatas
    )

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Create a chain that uses the Chroma vector store
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    # Let the user know that the system is ready
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()

    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]  # type: List[Document]

    text_elements = []  # type: List[cl.Text]

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            # Create the text element referenced in the message
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nSources: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    await cl.Message(content=answer, elements=text_elements).send()
