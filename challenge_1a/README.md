# Adobe-Hack - 1A - PDF Extraction of Headings

A smart PDF heading extraction tool using machine learning, powered by pdfminer.six and scikit-learn. It processes PDFs and outputs structured outlines with heading levels (`H1`, `H2`, etc.) in JSON format.

---

## Approach

This project tackles the challenge of automatically identifying and classifying headings in PDF documents using a machine learning approach. The solution is built around the following methodology:

### 1. Text Span Extraction

The system uses **pdfminer.six** to extract individual text spans from PDF pages, capturing not just the text content but also crucial formatting metadata including:

- Font name and size
- Character positioning
- Text styling attributes

### 2. Feature Engineering

Each extracted text span is analyzed and converted into a feature vector containing:

- **Font Properties**: Size, bold/italic styling, font family
- **Text Characteristics**: Length, case pattern (uppercase, lowercase, sentence case, mixed)
- **Structural Indicators**: Numeric prefixes (1., A., i.), bullet points, indentation
- **Relative Sizing**: Comparison with the most common font size in the document

### 3. Machine Learning Classification

A **DecisionTreeClassifier** is trained on labeled data to classify text spans into categories:

- **H1, H2, H3, etc.**: Different heading levels
- **P**: Paragraph/body text
- **Other**: Non-heading, non-paragraph content

The model uses preprocessing steps including:

- Label encoding for categorical features (text case)
- Feature scaling for numerical attributes (font size, text length)
- Balanced training on diverse document types

### 4. Hierarchical Structure Building

The classified spans are processed to build a structured document outline:

- Headings are organized by their hierarchical levels
- Page numbers are tracked for each heading
- Document title is extracted (typically the first bold H1 or the first heading found)

### 5. Output Generation

Results are serialized into clean JSON format containing:

- Document title
- Hierarchical outline with heading levels, text content, and page references

This approach leverages the fact that headings in professional documents typically follow consistent visual patterns (larger fonts, bold styling, specific positioning) that can be learned and generalized across different document types.

### Research Foundation

This implementation draws heavily from the research paper ["A Supervised Learning Approach For Heading Detection"](https://arxiv.org/pdf/1809.01477) by Budhiraja & Mago (2018), which demonstrated that machine learning classifiers can achieve high accuracy (96.95%) in heading detection tasks. Their work showed that features like font properties, text characteristics, and structural indicators are highly predictive for heading classification.

To achieve comparable accuracy, this project involved **manual labelling of over 1,500 data points** extracted from diverse PDF documents, ensuring robust training data across different document types and formatting styles. By adapting their methodology and feature engineering techniques combined with our comprehensive labeled dataset, we were able to achieve an impressive **accuracy of 97.3%** - surpassing the original research results.

---

## Features

- Extracts text spans from PDFs
- Classifies headings using a trained ML model
- Uses font size, bold/italic style, numbering, casing, and bullets as features
- Outputs structured JSON outlines
- Dockerized for easy deployment

---

## Project Structure

```
adobe-hack/
├── input/                  # Input PDF files
├── output/                 # Output JSON files
├── csvs/                   # Contains training data csv file
├── models/                 # Pre-trained ML models
│   ├── model.pkl
│   ├── le_case.pkl
│   ├── le_label.pkl
│   └── scaler.pkl
├── main.py                 # Main heading extraction script
├── requirements.txt
├── Dockerfile
├── .gitignore
├── csv_generation.py       # Script to generate the training csv file
└── README.md
```

---

## Model Info

The model is a DecisionTreeClassifier trained on labeled PDF spans using:

- Font size
- Bold/Italic attributes
- Text length
- Numbering/Bullet patterns
- Casing (e.g., UPPERCASE, Title Case)
- Relative font size (compared to common body text)

---

## Run with Docker

### 1. Clone the repository

```bash
git clone https://github.com/pranayyb/adobe-hack.git
cd adobe-hack/challenge_1a
```

### 2. Add PDFs to the `/input` directory

Place your `.pdf` files inside the `input/` folder.

### 3. Build the Docker image

```bash
docker build -t adobe1a .
```

### 4. Run the container

```bash
docker run --rm \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/output \
  adobe1a
```

Output `.json` files will appear in the `/output` directory.

---

## Sample Output

```json
{
  "title": "Sample Document",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 },
    { "level": "H3", "text": "Previous Work", "page": 2 }
  ]
}
```

---

## Tech Stack

- **Python 3.10**
- **pdfminer.six** - PDF text extraction
- **scikit-learn** - Machine learning models
- **pandas** - Data processing
- **Docker** - Containerization

---

## Local Development

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/pranayyb/adobe-hack.git
cd adobe-hack
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the script:

```bash
python main.py
```

5. Deactivate virtual environment (when done):

```bash
deactivate
```

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
- pdfminer.six community for the excellent PDF processing library
- scikit-learn team for the machine learning framework
