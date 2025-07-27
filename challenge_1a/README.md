# Adobe-Hack

A smart PDF heading extraction tool using machine learning, powered by pdfminer.six and scikit-learn. It processes PDFs and outputs structured outlines with heading levels (`H1`, `H2`, etc.) in JSON format.

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
cd adobe-hack
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
