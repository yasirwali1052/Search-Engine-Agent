import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain_classic.agents import initialize_agent, AgentExecutor, AgentType
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
import os
from dotenv import load_dotenv

## Arxiv and wikipedia Tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

search=DuckDuckGoSearchRun(name="Search")


st.title("🧠 AI Assistant with Smart Search")

"""
Ask anything! This AI can explore the web, Wikipedia, or Arxiv to help you.  
Watch its thinking live using Streamlit’s callback handler.
"""


## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

if prompt:=st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    llm=ChatGroq(groq_api_key=api_key,model_name="openai/gpt-oss-120b",streaming=True)
    tools=[search,arxiv,wiki]

    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        # Get the last user message
        user_message = st.session_state.messages[-1]["content"]
        
        try:
            search_agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True
            )
            response = search_agent.run(user_message, callbacks=[st_cb])
            final_response = response
        except Exception as e:
            st.error(f"Error: {str(e)}")
            final_response = f"Sorry, I encountered an error: {str(e)}"
        
        st.session_state.messages.append({'role':'assistant',"content":final_response})
        st.write(final_response)
