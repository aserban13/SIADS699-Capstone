

import pandas as pd
# Need this set to None otherwise text columns will truncate!
pd.set_option('display.max_colwidth', None) 

# NLP
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def text_embeddings(data, text_column_name, model = "multi-qa-mpnet-base-dot-v1"):
    model = SentenceTransformer(model)
    text_to_encode = data[text_column_name]
    embeddings = model.encode(text_to_encode)
    return embeddings

def compute_similarity_scores(query, embeddings, model = "multi-qa-mpnet-base-dot-v1"):
    
    model = SentenceTransformer(model)
    # Convert query to embedding
    query_embedding = model.encode(query)
    
    # Compute cosine similarity between query and all embeddings
    similarity_scores = cosine_similarity(query_embedding.reshape(1, -1), embeddings)

    # reshape to to fit on df
    return similarity_scores.reshape(-1, 1)  # Return similarity scores for all rows