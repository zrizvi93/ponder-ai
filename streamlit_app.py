import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

from langchain_helper import load_or_parse_data


load_dotenv()


st.set_page_config(page_title="Chatting with Don Quixote, using LangChain 🦜️🔗", page_icon="🔗", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chatting with Don Quixote, using LangChain 🦜️🔗")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Don Quixote!"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the book!"):
        
        chunks = load_or_parse_data()
        embeddings_model = OpenAIEmbeddings()
        index = Chroma.from_documents(chunks, embeddings_model)

        return index


index = load_data()
retriever = index.as_retriever(search_kwargs={"k": 10})

if "rag_chain" not in st.session_state.keys(): # Initialize the chat engine
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        template = """You are an a helpful and knowledgeable reading companion. 
            Use the following pieces of retrieved context to answer the reader's question. 
            If you don't know the answer, just say that you don't know. 
            Use three sentences maximum and keep the answer concise.
            Question: {question} 
            Context: {context} 
            Answer:
            """
        prompt = ChatPromptTemplate.from_template(template)
        st.session_state.rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        )

if user_query := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_chain.invoke(user_query)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history

