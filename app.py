from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os
import git
import glob
import chromadb
import pandas as pd
import uvicorn
import asyncio

load_dotenv()

# Configuration
DATA_PATH = "data/"
EMBEDDINGS_PATH = "embeddings/"
ALLOWED_EXTENSIONS = {".py", ".java", ".c", ".cpp", ".js", ".ts", ".html", ".css", ".rb", ".php", ".swift", ".go",
                      ".rs", ".kt", ".kts", ".sql", ".sh", ".r", ".hs", ".pl"}
REPO_LIST = [
    "https://github.com/dodona-edu/dolos",
    "https://github.com/jplag/JPlag",
    "https://github.com/blingenf/copydetect"
]

# Ensure directories exist
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(EMBEDDINGS_PATH, exist_ok=True)


# Clone repositories
def clone_repos():
    for repo_url in REPO_LIST:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(DATA_PATH, repo_name)

        if not os.path.exists(repo_path):
            print(f"Cloning {repo_url} into {repo_path}...")
            git.Repo.clone_from(repo_url, repo_path)
        else:
            print(f"Repository {repo_name} already exists.")


# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Initialize vector database (ChromaDB)
chroma_client = chromadb.PersistentClient(path=EMBEDDINGS_PATH)
collection = chroma_client.get_or_create_collection("code_embeddings")


def get_code_files():
    files = []
    for ext in ALLOWED_EXTENSIONS:
        files.extend(glob.glob(f"{DATA_PATH}/**/*{ext}", recursive=True))
    return files


def process_files():
    for file_path in get_code_files():
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        # Generate embedding
        embedding = model.encode(code).tolist()

        # Store in vector DB
        collection.add(
            ids=[file_path],
            embeddings=[embedding],
            metadatas=[{"path": file_path}]
        )


# FastAPI service
app = FastAPI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.post("/check_plagiarism/")
async def check_plagiarism(code_snippet: str):
    try:
        # Generate embedding
        snippet_embedding = model.encode(code_snippet).tolist()

        # Search vector DB
        results = collection.query(query_embeddings=[snippet_embedding], n_results=3)

        if not results['ids']:
            return {"plagiarism": "No similar code found"}

        similar_files = results['metadatas'][0]

        # Check with LLM
        prompt = f"""
        User submitted the following code snippet:
        ```
        {code_snippet}
        ```
        Below are similar code files from the repository:
        {similar_files}

        Is this plagiarism? Respond with 'Yes' or 'No' only.
        """

        response = OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        return {
            "plagiarism": response['choices'][0]['message']['content'],
            "similar_files": similar_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Evaluation script
def evaluate_system():
    test_cases = [
        {"code": "def add(a, b): return a + b", "expected": "Yes"},
        {"code": "def multiply(a, b): return a * b", "expected": "No"}
    ]
    results = []

    for case in test_cases:
        response = asyncio.run(check_plagiarism(case["code"]))
        results.append({
            "code": case["code"],
            "expected": case["expected"],
            "actual": response["plagiarism"]
        })

    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    print("Evaluation complete. Results saved to evaluation_results.csv")


if __name__ == "__main__":
    clone_repos()
    process_files()
    evaluate_system()
    uvicorn.run(app, host="0.0.0.0", port=8000)