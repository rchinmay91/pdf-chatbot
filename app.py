import os
import gradio as gr

# Modern stable import structures
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEmbeddings,
    HuggingFaceEndpoint,
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# =====================================================================
# 1. INITIALIZE ENVIRONMENT & MODELS
# =====================================================================
# Pulls standard secret from Hugging Face Space environment
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN or HF_TOKEN == "":
    # Paste your actual hf_... token string here for testing on your local machine
    HF_TOKEN = "hhhhhhhhhhhhhhhhh" 

# Initialize cloud embedding weights
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# FIXED: Swapped to a highly available, modern model and task type
base_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation", # Standard compatible task type for Qwen structure
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=512,
)

# Keep it wrapped to enforce the chat interface conversion layer
llm = ChatHuggingFace(llm=base_llm)



# =====================================================================
# 2. DOCUMENT PROCESSING ENGINE (RAG)
# =====================================================================
def process_pdf(file):
    global vector_store, retriever
    if file is None:
        return "⚠️ Please upload a valid PDF file."
    
    try:
        # Load and parse PDF structure using community loader
        loader = PyPDFLoader(file.name)
        documents = loader.load()
        
        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Load chunks into Chroma Vector DB
        vector_store = Chroma.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        return "✅ Document indexed successfully! Start chatting below."
    except Exception as e:
        return f"❌ Error processing document: {str(e)}"

# Helper function to format document context snippets
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# =====================================================================
# 3. INTERACTIVE CHAT ENGINE (UPGRADED FOR GRADIO 6.0+ OBJECTS)
# =====================================================================
def respond_chat(message, history):
    global retriever
    if retriever is None:
        return "⚠️ Setup incomplete. Please upload and index a PDF file first."

    try:
        # 1. Properly parse modern Gradio ChatMessage objects (.role and .content)
        formatted_history = ""
        for turn in history:
            # Check if history elements are modern object classes or standard dicts
            role = getattr(turn, "role", None) or turn.get("role")
            content = getattr(turn, "content", None) or turn.get("content")

            if role == "user":
                formatted_history += f"Human: {content}\n"
            elif role == "assistant":
                formatted_history += f"AI: {content}\n"

        # 2. Reformulate standalone question if chat history exists
        if formatted_history:
            condense_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Given the following chat history and a follow-up question, rephrase the follow-up question to be a standalone question contextually aware of the history.\n\nChat History:\n{chat_history}",
                    ),
                    ("human", "{input}"),
                ]
            )
            condense_chain = condense_prompt | llm | StrOutputParser()
            standalone_query = condense_chain.invoke(
                {"chat_history": formatted_history, "input": message}
            )
        else:
            standalone_query = message

        # 3. Retrieve relevant context document chunks
        retrieved_docs = retriever.invoke(standalone_query)
        context_text = format_docs(retrieved_docs)

        # 4. Generate final answer utilizing strictly retrieved facts
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert document assistant. Answer the user's question using exclusively the provided retrieved text context. If you do not know the answer or if it's not present in the context, explicitly state that you cannot find the answer in the document. Limit responses to three clear concise sentences.\n\nContext:\n{context}",
                ),
                ("human", "{input}"),
            ]
        )

        qa_chain = qa_prompt | llm | StrOutputParser()
        answer = qa_chain.invoke(
            {"context": context_text, "input": standalone_query}
        )

        return answer
    except Exception as e:
        return f"❌ Inference failed: {str(e)}"


# =====================================================================
# 4. USER INTERFACE
# =====================================================================
with gr.Blocks(title="Cloud PDF RAG Chatbot") as demo:
    gr.Markdown("# 📚 Private PDF Chatbot (Cloud API Framework)")
    gr.Markdown("Upload your documents to execute lightning-fast chat queries completely free.")
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(label="Upload Document (PDF)", file_types=[".pdf"])
            status_output = gr.Textbox(label="System Status", interactive=False, value="Awaiting PDF...")
            process_btn = gr.Button("Analyze & Index", variant="primary")
            
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(fn=respond_chat)
            
    process_btn.click(fn=process_pdf, inputs=[pdf_input], outputs=[status_output])

if __name__ == "__main__":
    demo.launch()
