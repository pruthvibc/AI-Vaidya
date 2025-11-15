import os
from flask import Flask, render_template, request, jsonify
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI

# -------------------- OPENAI CLIENT --------------------
client = OpenAI(api_key="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")   # <<< PUT YOUR KEY

# -------------------- FLASK APP ------------------------
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------- MODELS ----------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------- MEMORY ----------------------------
text_chunks = []
embeddings = None
faiss_index = None


# -------------------- HELPERS ----------------------------
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    return text


def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks


def build_embeddings(chunks):
    global embeddings, faiss_index
    embeddings = embedding_model.encode(chunks, convert_to_numpy=True)
    faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss_index.add(embeddings)


# -------------------- FIXED generate_answer --------------------
def generate_answer(question, retrieved_text):
    prompt = f"""
    You are an Ayurveda expert. Answer the question using the reference text below.

    Reference Text:
    {retrieved_text}

    Question: {question}

    Give a clear, correct, simplified answer.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()


# ------------------------ ROUTES -------------------------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global text_chunks

    file = request.files['file']
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    text = extract_text(file_path)
    text_chunks = chunk_text(text)

    build_embeddings(text_chunks)

    return jsonify({"status": "success", "message": "Book uploaded and processed!"})


@app.route('/ask', methods=['POST'])
def ask_question():
    global text_chunks, faiss_index

    question = request.form['question']

    if not text_chunks or faiss_index is None:
        return jsonify({"answer": "Please upload a book first!", "reference": ""})

    # Encode question
    q_embedding = embedding_model.encode([question], convert_to_numpy=True)

    # Retrieve relevant chunks
    D, I = faiss_index.search(q_embedding, k=3)
    retrieved_chunks = [text_chunks[i] for i in I[0]]
    reference_text = "\n\n".join(retrieved_chunks)

    # Generate answer
    answer = generate_answer(question, reference_text)

    return jsonify({
        "answer": answer,
        "reference": reference_text
    })


if __name__ == "__main__":
    app.run(debug=True)
