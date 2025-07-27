from sentence_transformers import SentenceTransformer

model_id = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(model_id)
model.save("./minilm")
