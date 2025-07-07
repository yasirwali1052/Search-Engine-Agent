
# 🔍 AI Chatbot with Web Search (LangChain + Streamlit + Groq)

This is a smart chatbot built with **LangChain**, **Streamlit**, and **Groq's LLaMA 3** model. It answers your questions using three tools:  
🌐 DuckDuckGo (Web Search) | 📚 Wikipedia | 🧪 Arxiv (Research Papers).  
It also shows the agent’s reasoning step-by-step using Streamlit callbacks.

---

## 🧠 How It Works (Code Flow)

- `Streamlit` builds the UI for chat and sidebar input.
- User enters a **Groq API key** in the sidebar.
- Chat history is saved in `st.session_state["messages"]`.
- When the user asks a question:
  - It initializes **ChatGroq** using LLaMA3 model.
  - A LangChain **ReAct Agent** is created with 3 tools:
    - `DuckDuckGoSearchRun`
    - `WikipediaQueryRun`
    - `ArxivQueryRun`
  - The agent decides which tool(s) to use.
  - While searching, it shows real-time thought steps using `StreamlitCallbackHandler`.
  - The final answer is displayed and added to chat history.

---

## 🚀 Run This Project

1. **Clone the repo**
   ```bash
   git clone https://github.com/yasirwali1052/Search-Engine-Agent
   cd your-repo
````

2. **Create & activate Conda environment**

   ```bash
   conda create -n agents python=3.10
   conda activate agents
   ```

3. **Install packages**

   ```bash
   pip install streamlit langchain langchain-community langchain-ollama duckduckgo-search python-dotenv faiss-cpu
   ```

4. **Add `.env` file with your Groq key**

   ```
   GROQ_API_KEY=your_groq_key_here
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

