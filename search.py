import faiss
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
import pymongo


def text_embed(query):
    embedding_query = embeddings.embed_query(query)
    return np.array([embedding_query])


class fs:

    def __init__(self, raw, top_k=-1):
        self.top_k = top_k
        self.index = faiss.IndexFlatL2(768)
        self.index.add(raw)

    def faiss_similar(self, embedding):
        top_k = self.index.ntotal
        scores, indices = self.index.search(embedding, top_k)
        scores = scores[0].tolist()
        indices = indices[0].tolist()
        self.scores = dict(zip(indices, scores))

    
    # def tag_similar(self, tags_embedding):
    #     tags_embedding

query = ""
embeddings = HuggingFaceEmbeddings()   
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["photoshop"]
collection = db["pexel_photo"]


raw_data = [(i["title"], i["tags"], i["url"]) for i in collection.find({})]
raw_title = embeddings.embed_documents([i[0] for i in raw_data])
raw_title = np.array(raw_title)
# tag_faiss = fs(raw_tag)
title_faiss = fs(raw_title)


def search(query, topk=6):
    embedding_query = text_embed(query)
    # tag_faiss.faiss_similar(embedding_query)
    title_faiss.faiss_similar(embedding_query)
    res = sorted(title_faiss.scores.items(), key=lambda x: x[1], reverse=True)
    top_res = [i[0] for i in res][: topk]
    return [raw_data[i][2] for i in top_res]