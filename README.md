🌿 AI Vaidya- Ayurveda AI Knowledge Assistant

Transforming unstructured Ayurveda knowledge into instant, reliable answers.

📝 Project Title and Problem Statement

Project Title: Ayurveda AI Knowledge Assistant

Problem Statement:
Ayurveda holds vast knowledge across books, research papers, and articles. However, this knowledge is often scattered, unstructured, and hard to access. Students, practitioners, and enthusiasts struggle to quickly find reliable information.

Our solution: A smart AI system that reads Ayurveda texts, understands their content, and answers user queries in plain English, without needing the internet.

💡 Solution Overview

What it does:

Ingests Ayurveda books, research papers, and articles.

Understands the content using AI models.

Provides natural language answers to user queries.

Key Features:

Text Ingestion: Upload and process PDFs, articles, and e-books.

Semantic Search: Finds the most relevant text based on user questions.

AI-Powered Q&A: Generates concise and accurate answers in English.

Offline Knowledge Base: Uses only provided texts, no internet required.

Benefit: Users can get instant, accurate answers without reading multiple sources manually.

⚙️ Technical Architecture

1. Data Processing:

Text cleaning, chunking, and formatting.

Convert text into embeddings (semantic vectors).

2. Model Usage:

Language model processes user queries.

Vector search retrieves relevant text chunks.

AI generates answers based on retrieved content.

3. User Flow:

User asks a question in English.

Query is converted to embedding.

System searches vector database for relevant content.

AI generates and displays the answer.

Architecture Diagram:

[Ayurveda Texts] --> [Text Preprocessing & Embeddings] --> [Vector Database]
         ↑                                                   |
         |                                                   ↓
       [User Query] --> [Query Embedding & Retrieval] --> [AI Model] --> [Answer]

🛠️ APIs / Libraries Used

Python Libraries:

transformers (Hugging Face)

sentence-transformers

FAISS / Chroma (Vector Search)

Streamlit (Frontend Interface)

PyPDF2 / pdfplumber (PDF reading)

numpy, pandas (Data processing)

Open-Source Models:

Pretrained Transformer models (e.g., GPT or BERT variants)

🚀 Future Scope

Support for multi-language queries (Sanskrit, Hindi).

Voice-based Q&A for accessibility.

Image recognition for Ayurvedic herbs and plants.

Mobile application for wider reach.

Continuous knowledge base updates with new research.

🎯 How to Run

Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py


Upload Ayurveda texts and start asking questions.