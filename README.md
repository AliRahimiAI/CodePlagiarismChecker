# Code Plagiarism Checker

## Description
The **Code Plagiarism Checker** is a FastAPI-based system designed to detect code plagiarism using vector embeddings and OpenAI's GPT-4 model. It compares the provided code snippet with a repository of existing code and determines whether plagiarism exists based on semantic similarity.
This is a simple system I tried to build to test my new knowledge on ML engineering.

### Key Features:
- **Code Embedding**: Converts code into vector embeddings using a pre-trained model from Hugging Face.
- **Plagiarism Detection**: Uses a combination of vector similarity search and OpenAI GPT-4 to identify potential code plagiarism.
- **FastAPI**: Provides a simple and fast API to check for plagiarism.
- **Dockerized**: The system can be run in a containerized Docker environment for easy deployment and portability.

---

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine using Git:

```bash
git clone https://github.com/your-username/code-plagiarism-checker.git
cd code-plagiarism-checker
```

### 2. Install Dependencies
Install the required Python dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### 3. Run the Service
You can run the plagiarism checker service locally using the following command:

```bash
python main.py
```

This will start the FastAPI service at `http://localhost:8000`.

### 4. Docker Setup
If you prefer to run the system inside a Docker container, follow these steps:

- **Ensure Docker is installed** on your machine. You can download Docker Desktop from [here](https://www.docker.com/products/docker-desktop).
  
- **Build the Docker Image**:
  In the root directory of the project, run the following command to build the Docker image:

  ```bash
  docker build -t plagiarism-checker .
  ```

- **Run the Docker Container**:
  After building the image, you can run the application in a Docker container with the following command:

  ```bash
  docker run -p 8000:8000 plagiarism-checker
  ```

This will expose the FastAPI application on port 8000. You can now access the API at `http://localhost:8000`.

---

## API Usage

The API endpoint to check code plagiarism is `/check_plagiarism/`. You can make a POST request to this endpoint with the following JSON payload:

### Endpoint
- **URL**: `/check_plagiarism/`
- **Method**: `POST`

### Request Body
You need to send a **code snippet** that you want to check for plagiarism in the request body as a JSON object:

```json
{
  "code_snippet": "<code_here>"
}
```

Replace `<code_here>` with the actual code snippet you want to check.

### Example Request:
```bash
curl -X 'POST' \
  'http://localhost:8000/check_plagiarism/' \
  -H 'Content-Type: application/json' \
  -d '{
  "code_snippet": "def hello_world():\n    print('Hello, world!')"
}'
```

### Example Response:
```json
{
  "is_plagiarism": "no",
  "similar_code_files": []
}
```

The response contains:
- **is_plagiarism**: A string that indicates whether the code is plagiarized ("yes" or "no").
- **similar_code_files**: A list of code files from the database that are similar to the provided code snippet (only included if plagiarism is detected).

---

## Evaluation

To evaluate the performance of the plagiarism detection system, the `main.py` script automatically runs tests. These tests check the system’s functionality and ensure everything is working correctly.

To manually trigger the evaluation and tests, run the following command:

```bash
python main.py
```

This will execute the system and run the pre-defined tests to evaluate the system's accuracy.

---

## Folder Structure

Here is a brief overview of the folder structure of this project:

```
.
├── app.py                # Main FastAPI application that runs the plagiarism checker API
├── dockerfile            # Docker configuration file to build the Docker image
├── requirements.txt      # Python dependencies
├── test_plagiarism.py    # Unit tests to evaluate plagiarism detection logic
├── README.md             # This README file
└── data/                 # Folder for storing cloned repositories and embeddings
```

- **app.py**: The main entry point of the FastAPI app where the plagiarism check logic resides.
- **dockerfile**: The Docker configuration file that helps in building and running the application inside a container.
- **test_plagiarism.py**: Contains unit tests to verify the functionality of the plagiarism detection system.

---

## Technologies Used

- **FastAPI**: Framework for building the web API.
- **Hugging Face Transformers**: For using pre-trained models to create code embeddings.
- **OpenAI GPT-4**: For fine-tuning and detecting plagiarism in code.
- **Docker**: To containerize the application for easy deployment.
- **Faiss / ChromaDB**: Vector databases used to store and search code embeddings.

---

## Troubleshooting

- **Docker Issues**: Ensure Docker is installed and running properly on your machine. Refer to the official Docker documentation for troubleshooting if you're encountering Docker-related errors.
  
- **WSL2 Issues**: If you're running this project on Windows, make sure that WSL2 is enabled, along with the necessary virtual machine platform and virtualization settings. Follow the instructions [here](https://aka.ms/enablevirtualization) to resolve WSL2 issues.

- **Dependency Issues**: If you encounter issues with dependencies, try creating a new Python virtual environment and installing the dependencies again:

  ```bash
  python -m venv venv
  source venv/bin/activate  # For Linux/MacOS
  venv\Scripts\activate     # For Windows
  pip install -r requirements.txt
  ```

---

Feel free to open an issue on the repository if you encounter any problems or have suggestions for improvement!

--- 
