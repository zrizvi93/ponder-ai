# ponder-ai

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Try out the app

Once the app is loaded, enter your question about the Streamlit library and wait for a response.


## Local Dev Loop

`pyenv local`
Use python version in .python-version file


`virtualenv -v venv-ponder-ai && source venv-ponder-ai/bin/activate`
Create and activate virtual environment


`touch .env`
From project root, create environment variable file and add the following variables ([Reference](https://docs.datastax.com/en/astra/astra-db-vector/integrations/llamaindex.html))
```
OPENAI_API_KEY="API_KEY"
```

`mkdir data`
From project root, create data/ directory which will store text and pickle files


`pip install -r requirements.txt`
Install deps


`streamlit run streamlit_app.py`
Run app from the project root


The dev server can be accessed at [localhost:8501](http://localhost:8501/)


Additional Notes:

`kill -9 $(lsof -i:8501 -t) 2> /dev/null`
To quickly kill any process running on port 8501

