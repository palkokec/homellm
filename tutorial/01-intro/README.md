This is just a short introduction to tutorial series.
It should provide you an overview of tooling used in tutorials.

# Rather long intro
**Prompt:**
> please write an introductory paragraph in md notation about intention to write tutorial series on usage of opensource LLM at home on low resources hardware. The paragraph should be max 500 words long.

**Answer:**
> Welcome to the exciting world of open-source language models (LLMs) and the upcoming tutorial series that aims to empower you to harness the capabilities of these advanced language models on low-resource hardware in the comfort of your home. As technology continues to advance, the accessibility of powerful language models has become a reality, opening up new possibilities for natural language understanding and generation. However, many individuals may be limited by hardware constraints, preventing them from fully experiencing the potential of these models. This tutorial series is designed to bridge that gap by providing step-by-step guidance on setting up and utilizing open-source LLMs efficiently on low-resource devices. Whether you're a student, hobbyist, or simply curious about the capabilities of language models, this series will cater to your needs, ensuring that you can explore and leverage the potential of open-source LLMs without the need for high-end hardware. Get ready to embark on a journey that will demystify the process of working with language models, enabling you to tap into their power and applications within the confines of your home and modest computing resources. Let's unlock the full potential of open-source LLMs and make the most of what they have to offer in your everyday computing endeavors!

This is just one of the examples, how LLM can help you and most probably you are using some service like [ChatGPT](https://chat.openai.com) already. But what if you do not want to share your data with external services, pay other providers, or simply get to more complex use cases and have more control over LLM.

This tutorial series will try to guide you through some approaches how to use LLM models locally.

# HW & SW

All the code was executed and succesfully run on my home personal computer (5+ years old):

* **Processor:** Intel® Core™ i7-4790 CPU @ 3.60GHz × 8 
* **RAM:** 16G
* **GPU:** integrated Mesa Intel® HD Graphics 4600 (HSW GT2)
* **OS:** Debian 12

There are variety of tools which can be used for work with LLM models, but this tutorial will focus on the toolset I found proven to work reliably on the low resource HW.

## Python + Langchain + Huggingface + nltk + chainlit

* [Python](https://www.python.org/) is programming language used in data science, it has good community support and large amount of libraries to integrate with LLMs. Therefore it is the choice of language for this tutorial. Later in series I might touch other languages like RUST, NodeJS or even Java. We will be using Python 3.11+ with virtualenv throughout the series.

* [Langchain](https://python.langchain.com/docs/get_started/introduction) is a framework for developing applications powered by language models. Best support is in Python or NodeJS

* [Huggingface](https://huggingface.co/) is basically GitHub for language models. We will be downloading the resources and interacting with huggingface in our code.

* [nltk](https://www.nltk.org/) python natural language toolktit. We will be usng it later for more complex examples and building our LLM models from scratch.

* [chainlit](https://docs.chainlit.io/get-started/overview) is an open-source Python package that provides Chat GPT like UI to quickly built the chat applicationswith your own business logic and data. We will be using it in some examples to interact with LLM.

## Llama.cpp

[Llama.cpp](https://github.com/ggerganov/llama.cpp) is a plain C/C++ implementation without dependencies implementation of LLaMA model. The project provides also tooling for model conversion and python langchain libraries are available to integrate with supported model format.

## Docker

[Docker](https://www.docker.com/) is a platform to run container applications. We will be using it to run some software in container instead of deploying it locally.

## ChromaDB

[ChromaDB](https://docs.trychroma.com/) is the open-source embedding(vector) database. We will be using it to store the embeddings in some use cases.

## PostgreSQL

[PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database. We will be using it in some use cases to persist some metadata.

## Apache Tika

[Tika](https://tika.apache.org/) toolkit detects and extracts metadata and text from over a thousand different file types (such as PPT, XLS, and PDF). We will be using it for metadata and data preparation.

## RTG

[Reader-Translator-Generator](https://cutelab.name/rtg/#_overview) is a Neural Machine Translation toolkit based on pytorch. We will be using it in some use case instead of pblic services to perform document translations.