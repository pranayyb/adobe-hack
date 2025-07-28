# Adobe-Hack - 1B - PDF Section Ranking and Analysis

A semantic PDF section analysis tool that processes multiple PDF documents, extracts structured sections, and ranks them by relevance to a given persona and job description using SentenceTransformer models.

---

## Approach

This project addresses the challenge of intelligently analyzing and ranking PDF content based on semantic relevance to specific user requirements. The solution employs a multi-stage approach that combines structural analysis with advanced natural language processing:

### 1. Structured Section Extraction

The system leverages the **Challenge 1A module** to extract hierarchical document structures from PDF files, including:

- **Heading Detection**: Uses the trained ML model (97.3% accuracy) to identify document headings at various levels (H1, H2, H3, etc.)
- **Content Extraction**: Captures paragraph content associated with each section and subsection
- **Metadata Preservation**: Maintains page numbers, document sources, and hierarchical relationships

### 2. Content Flattening and Preprocessing

Extracted hierarchical structures are flattened into a searchable format:

- **Section Consolidation**: Combines section headings with their associated paragraph content
- **Text Refinement**: Aggregates subsection paragraphs to create comprehensive section descriptions
- **Document Attribution**: Maintains traceability to source documents and page locations

### 3. Semantic Embedding Generation

The system uses **SentenceTransformer all-MiniLM-L6-v2** model for semantic understanding:

- **Model Performance**:
  - Sentence Embeddings: 68.06/100 (14 datasets)
  - Semantic Search: 49.54/100 (6 datasets)
  - Average Performance: 58.80/100
- **Model Specifications**:
  - Speed: 14,200 sentences/second
  - Model Size: 80 MB
  - 384-dimensional dense vector embeddings
- **Dense Vector Representation**: Converts both section content and user queries into high-dimensional embeddings
- **Contextual Understanding**: Captures semantic meaning beyond simple keyword matching
- **Efficient Processing**: Lightweight model optimized for production deployment with excellent balance of performance, speed, and resource efficiency

### 4. Query Construction and Matching

User requirements are transformed into effective search queries:

- **Persona Integration**: Combines user persona with specific job requirements
- **Query Embedding**: Generates semantic embeddings for the combined persona-job query
- **Similarity Computation**: Uses cosine similarity to measure semantic relatedness between sections and queries

### 5. Relevance Ranking and Selection

Sections are ranked based on semantic similarity scores:

- **Scoring Algorithm**: Computes cosine similarity between section embeddings and query embedding
- **Relevance Ranking**: Sorts sections by decreasing similarity scores
- **Top-K Selection**: Returns the 10 most relevant sections with importance rankings
- **Content Enrichment**: Includes both section titles and detailed paragraph content

### 6. Structured Output Generation

Results are formatted into comprehensive JSON output containing:

- **Metadata Tracking**: Documents processed, query parameters, processing timestamps
- **Ranked Sections**: Top sections with importance rankings and source attribution
- **Detailed Analysis**: Full paragraph content for in-depth understanding

This approach enables users to quickly identify the most relevant sections across multiple PDF documents based on their specific role and objectives, significantly reducing manual document review time while ensuring comprehensive coverage of relevant content.

---

## Features

- **PDF Processing**: Extracts structured sections and subsections from PDF documents using Challenge 1A module
- **Semantic Ranking**: Uses SentenceTransformer models to rank sections by relevance to queries
- **Flexible Querying**: Supports custom persona and job descriptions for targeted analysis
- **JSON Output**: Generates structured output with ranked sections and metadata
- **Top-K Selection**: Returns the top 10 most relevant sections with importance rankings
- **Dockerized**: Ready for containerized deployment

---

## Project Structure

```
challenge_1b/
├── main.py                    # Main application script
├── download_model.py          # Script to download SentenceTransformer model
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── README.md                  # This documentation
├── pdfs/                      # Input PDF files directory
│   ├── 1.pdf
│   ├── doc.pdf
│   ├── file02.pdf
│   └── file04.pdf
├── output/                    # Generated output files
│   └── challenge1b_output.json
└── minilm/                    # Downloaded SentenceTransformer model
    ├── 1_Pooling/
    ├── 2_Normalize/
    ├── config.json
    ├── model.safetensors
    └── ...
```

---

## Model Info

Uses **SentenceTransformer all-MiniLM-L6-v2** model for semantic similarity computation:

- **Performance Metrics**:
  - Sentence Embeddings: 68.06/100 (14 datasets)
  - Semantic Search: 49.54/100 (6 datasets)
  - Average Performance: 58.80/100
- **Model Specifications**:
  - Speed: 14,200 sentences/second
  - Model Size: 80 MB
  - Lightweight and optimized for production deployment
- **Functionality**:
  - Converts text sections and queries into 384-dimensional dense vector embeddings
  - Computes cosine similarity between section embeddings and query embedding
  - Ranks sections by semantic relevance score
  - Excellent balance of performance, speed, and resource efficiency

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- Docker (optional)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/pranayyb/adobe-hack.git
cd adobe-hack
```

### 2. Environment Setup

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Model

Before running the application, download the required SentenceTransformer model:

```bash
python download_model.py
```

This will download the MiniLM model to the `minilm/` directory.

### 5. Prepare Input PDFs

Place your PDF documents in the `pdfs/` directory. The application will process all PDF files found in this directory.

---

## Usage

### Command Line Interface

```bash
python main.py --persona "PERSONA_DESCRIPTION" --job "JOB_DESCRIPTION"
```

#### Required Arguments:

- `--persona`: Description of the persona (e.g., "A software engineer with expertise in agile methodologies")
- `--job`: Description of the job to be done (e.g., "Prepare a comprehensive analysis on agile testing methodologies")

#### Optional Arguments:

- `--input-dir`: Directory containing input PDF files (default: `./pdfs`)
- `--output-dir`: Directory for output JSON file (default: `./output`)
- `--model-path`: Path to the SentenceTransformer model (default: `./minilm`)

### Example Usage

```bash
python main.py \
  --persona "A software engineer with expertise in agile methodologies" \
  --job "Prepare a comprehensive analysis on agile testing methodologies, focusing on their evolution, current practices, and future trends"
```

---

## Run with Docker

### 1. Build the Docker image

```bash
docker build -t challenge1b .
```

### 2. Run the container

```bash
docker run --rm \
  -v "$(pwd)/challenge_1a/pdfs":/app/challenge_1b/pdfs \
  -v "$(pwd)/challenge_1b/output":/app/challenge_1b/output \
  challenge1b \
  --persona "A software engineer with expertise in agile methodologies" \
  --job "Prepare a comprehensive analysis on agile testing methodologies, focusing on their evolution, current practices, and future trends"
```

The Docker container includes a default command with sample persona and job description for agile testing methodologies.

---

## Sample Output

```json
{
  "metadata": {
    "input_documents": ["1.pdf", "doc.pdf", "file02.pdf"],
    "persona": "A software engineer with expertise in agile methodologies",
    "job_to_be_done": "Prepare a comprehensive analysis on agile testing methodologies...",
    "processing_timestamp": "2024-01-15T10:30:00.000Z"
  },
  "extracted_sections": [
    {
      "document": "doc.pdf",
      "section_title": "Agile Testing Fundamentals",
      "importance_rank": 1,
      "page_number": 5
    },
    {
      "document": "1.pdf",
      "section_title": "Test-Driven Development Practices",
      "importance_rank": 2,
      "page_number": 12
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc.pdf",
      "refined_text": "Detailed content about agile testing methodologies and their implementation in modern software development...",
      "page_number": 5
    }
  ]
}
```

---

## Tech Stack

- **Python 3.10**
- **sentence-transformers** - Semantic similarity computation
- **scikit-learn** - Cosine similarity calculations
- **numpy** - Numerical operations
- **pathlib** - File path handling
- **Docker** - Containerization

---

## Input Requirements

- **PDF Files**: Place PDF documents in the `pdfs/` directory
- **Dependencies**: Requires `challenge_1a` module for PDF processing functionality
- **Model**: SentenceTransformer model must be downloaded using `download_model.py`

---

## Local Development

### Running the Application

1. Ensure all setup steps are completed
2. Place PDF files in the `pdfs/` directory
3. Run with your desired persona and job:

```bash
python main.py \
  --persona "Your persona description" \
  --job "Your job description"
```

4. Check the `output/` directory for results

### Deactivate Environment

When done with development:

```bash
deactivate
```

---

## Troubleshooting

1. **Model Download Issues**: Ensure internet connectivity when running `download_model.py`
2. **PDF Processing Errors**: Verify PDFs are not corrupted and `challenge_1a` dependency is available
3. **Memory Issues**: For large PDF collections, consider processing smaller batches
4. **Import Errors**: Ensure the `challenge_1a` module is in the parent directory

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Pranay Buradkar**

- GitHub: [@pranayyb](https://github.com/pranayyb)

---

## Acknowledgments

- Adobe Hackathon for the inspiration
- SentenceTransformers library for semantic similarity computation
- scikit-learn team for machine learning utilities
- Challenge 1A module for PDF processing capabilities
