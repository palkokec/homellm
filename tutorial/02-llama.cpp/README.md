

We are starting with project llama.cpp. 
This can quickly get you running the LLm on your local HW.

# Example prompt

**Prompt:** 
>Python code to write data to postgresql database

**Answer:**
> # Import required modules
> import psycopg2
> from psycopg2 import sql
> # Connect to your postgres DB
> conn = psycopg2.connect(dbname='testDB', user='testUser', password='password', host='localhost')
> # Create a cursor object using the cursor() method
> cur = conn.cursor()
> # Execute a query
> cur.execute("INSERT INTO test_table (column1, column2) VALUES (%s, %s)", ('value1','value2'))
> conn.commit() # Commit your changes in the database
> # Fetch all rows using fetchall() method
> rows = cur.fetchall()
> for row in rows:
>     print("ID = ", row[0])
>     print("COLUMN1 = ", row[1], "\n")
> # Close communication with the database server
> cur.close()
> conn.close()

# Steps.

Clone the repo 

```
git clone git@github.com:ggerganov/llama.cpp.git
cd llama.cpp/
```

Build the app - this produces the **main** executable

```
make -j 16
```

Download the model from huggingface. Search for the gguf format of the models. The files in gguf format are usually provided in different bits size precision. Using 4bits or 5bits models is usually good compromise between the resource consumption and quality.

I am using GGUF file for [CodeNinja 1.0 Openchat 7B](https://huggingface.co/TheBloke/CodeNinja-1.0-OpenChat-7B-GGUF) model provided on HuggingFace.

Once model is downloaded you can start using it directly with Llama.cpp. 
See usage of the compiled binary:
```
 ./main --help

usage: ./main [options]

options:
  -h, --help            show this help message and exit
      --version         show version and build info
  -i, --interactive     run in interactive mode
  --interactive-first   run in interactive mode and wait for input right away
  -ins, --instruct      run in instruction mode (use with Alpaca models)
 ...
```

Here is an example how to use downloaded model in interactive mode

```
./main -i -m ~/workspace/data/models/codeninja-1.0-openchat-7b.Q5_K_S.gguf --interactive-first 
```
