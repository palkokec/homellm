# HomeLLM
My attempt to work with LLM on low resource hardware and to build the LLm in python working with my personal disk content.

## Tutorial section

To better understand and try out some of the concepts I've compiled tutorial section with explanation of tools I am using.
Each folder in tutorial section contains **Readme.md** file with further information.

## HomeLLM app

### Env setup

```
python3 -m venv .
. ./bin/activate
python3 -m pip install -r requirements.txt
```

### Metadata store
Using postgres pgvector to store tika metadata and chromadb for embeddings
```
docker build --build-arg PG_MAJOR=15 -t homellm/pgvector -f Dockerfile-pgvector .
docker run -d \
--name homellm-postgres \
-e POSTGRES_PASSWORD=homellm \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v /home/pali/workspace/data/pgdata:/var/lib/postgresql/data \
-p 5432:5432 \
homellm/pgvector
```
#### Meta database
```
python3 src/db_init.py 
```
```
psql -U postgres postgres 
DROP DATABASE IF EXISTS homellm;
CREATE DATABASE homellm LOCALE 'en_US.utf8' OWNER postgres;

CREATE TABLE files
(
  id BIGSERIAL PRIMARY KEY,
  filename VARCHAR(4095) NOT NULL,
  content_type VARCHAR(4095) NOT NULL,
  size BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  tika_status INT,
  tika_metadata JSON,
  stat_metadata JSON,
  language VARCHAR(10) NOT NULL
);  
```
```
docker pull chromadb/chroma
docker run -d \
--name homellm-chroma \
-e IS_PERSISTENT=TRUE \
-v /home/pali/workspace/data/chroma:/chroma/chroma/ \
-p 8000:8000 \
chromadb/chroma
```