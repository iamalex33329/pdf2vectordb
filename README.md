# PDF Upload and Vector Storage App

This application allows users to upload PDF files, process their content, generate embeddings, and store the information in a vector database. It provides a user-friendly interface for managing uploaded files and their associated data.

## Project Structure

The project consists of several Python files, each with a specific role:

- `main.py`: The main Streamlit application that handles the user interface and orchestrates the entire process.
- `core.db.models`:  This files defines a KnowledgeModel for storing and managing document data with fields for text, metadata, and a 1536-dimensional vector for embeddings.
- `core.db.operations`: This file provides functions for connecting to a LanceDB database, creating or opening tables, and performing CRUD operations on entries, using the KnowledgeModel schema.
- `core.pdf_processor.py`: Functions for extracting text content from PDF files.
- `core.embedding_generator.py`: Functions for generating embeddings from text using OpenAI's API.
- `utils.file_utils.py`: Utility functions for file operations, such as saving uploaded files and retrieving file information.

## Features

1. PDF File Upload: Users can upload multiple PDF files through the Streamlit interface.
2. File Processing: Uploaded PDFs are processed to extract their text content.
3. Embedding Generation: The extracted text is converted into vector embeddings using OpenAI's API.
4. Vector Storage: Embeddings and associated metadata are stored in a database.
5. File Management: Users can view uploaded files and delete them as needed.
6. Version Control: The system maintains different versions of the same file and can mark older versions as deprecated.
7. Soft Delete: Files are marked as deleted in the database but not immediately removed from the system.

## Dependencies

- Streamlit
- PyPDF2
- OpenAI
- python-dotenv

You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## Setup and Installation

1. Clone the repository.

2. Navigate to the repository directory:
    ```
    cd /path/to/repo
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Run the Streamlit application:
    ```
    streamlit run ./app/main.py
    ```

