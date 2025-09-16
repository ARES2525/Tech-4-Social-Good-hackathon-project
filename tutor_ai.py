import os
import pickle
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# =========================
# 1️⃣ Load API Key from .env or Environment
# =========================
load_dotenv()  # loads .env if available
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY. Please set it in your environment or .env file.")
    st.stop()

# =========================
# 2️⃣ Streamlit Setup
# =========================
st.set_page_config(page_title="Climate AI Tutor 🌱", page_icon="🌍", layout="wide")
st.title("🌍 Climate AI Tutor")
st.subheader("Ask me anything about climate change, sustainability, and eco-friendly actions!")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.3, 0.1)
age_group = st.sidebar.selectbox("Target Age Group", ["child", "teen", "adult"])
language = st.sidebar.selectbox("Preferred Language", ["English", "Hindi", "Spanish"])

# =========================
# 3️⃣ Load or Initialize FAISS (Cached)
# =========================
@st.cache_resource
def init_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists("climate_faiss.pkl"):
        with open("climate_faiss.pkl", "rb") as f:
            vectorstore = pickle.load(f)
    else:
        urls = [
            "https://climate.nasa.gov/evidence/",
            "https://www.ipcc.ch/report/ar6/syr/",
            "https://www.unep.org/resources/emissions-gap-report-2023"
        ]
        docs = []
        for url in urls:
            loader = WebBaseLoader(url)
            docs.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(split_docs, embeddings)
        with open("climate_faiss.pkl", "wb") as f:
            pickle.dump(vectorstore, f)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = init_retriever()

# =========================
# 4️⃣ Initialize Groq LLM (Cached)
# =========================
@st.cache_resource
def init_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",  # ✅ latest 70B model
        temperature=temperature,
        max_tokens=512
    )

llm = init_llm()

# =========================
# 5️⃣ Prompt Template
# =========================
template = """
You are a Climate Tutor AI.

- Adapt your answer to the age group: {age_group}.
- Use simple terms for children, relatable analogies for teens, and scientific accuracy for adults.
- Answer in the user's preferred language: {language}.
- Use the retrieved knowledge below to ensure accuracy:
{context}

User Question: {question}
"""

prompt = PromptTemplate(
    input_variables=["age_group", "language", "context", "question"],
    template=template
)

# =========================
# 6️⃣ User Input & Response
# =========================
user_prompt = st.text_area("✍️ Enter your climate question or topic:", placeholder="e.g., How does deforestation affect global warming?")

if st.button("🔎 Get Answer"):
    if not user_prompt.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Fetching info and generating AI response (may take time for 70B model)..."):
            try:
                # Retrieve relevant docs
                docs = retriever.invoke(user_prompt)
                context = "\n\n".join([d.page_content for d in docs])

                # Format prompt
                final_prompt = prompt.format(
                    age_group=age_group,
                    language=language,
                    context=context,
                    question=user_prompt
                )

                # Get AI response
                response = llm.invoke(final_prompt)
                st.success("✅ AI Response:")
                st.write(response.content)
            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# 7️⃣ Suggested Questions
# =========================
st.markdown("---")
st.markdown("💡 **Try asking:**")
examples = [
    "What are the top 5 renewable energy sources?",
    "Explain carbon footprint in simple terms for kids.",
    "How can schools reduce their energy consumption?",
    "What are the effects of plastic pollution on oceans?",
]
for ex in examples:
    st.code(ex, language="text")

st.markdown("🌱 *Powered by Groq AI*")
