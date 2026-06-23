from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from  langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("my_api")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

def load_all_docs(pdf_path=None):
    docs = []
    if os.path.exists("scraped_data/"):
        web_loader = DirectoryLoader("scraped_data/", glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        docs.extend(web_loader.load())
    if pdf_path and os.path.exists(pdf_path):
        pdf_loader = PyPDFLoader(pdf_path)
        docs.extend(pdf_loader.load())
    return docs
def build_chain(pdf_path = None):

    docs = load_all_docs(pdf_path)
    if not docs:                          # ✅ catch empty docs
        raise ValueError("No documents found. Add files to scraped_data/ or upload a PDF.")

    text_split = CharacterTextSplitter(separator=" ", chunk_size=2000, chunk_overlap=200)
    chunks = text_split.split_documents(docs)
    if os.path.exists("faiss_index"):
        vector_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        vector_db = FAISS.from_documents(chunks, embeddings)
        vector_db.save_local("faiss_index")
    retriever = vector_db.as_retriever(search_kwargs = {"k":3})
    prompt_template = ChatPromptTemplate.from_template("""
                                                       Answer The question Based only on the Context Below.
                                                       Context: {context}
                                                       Question : {question}""")
    chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
    )

    return chain
def llm_answer(user_input : str, chain):
    if user_input:
        an = chain.invoke(user_input)
        print(an)
        return an
    return "No input provided"