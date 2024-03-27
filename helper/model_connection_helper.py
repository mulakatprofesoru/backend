import sys
sys.path.append("..")

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

class ModelConnectionHelper:
    def __init__(self) -> None:
        pass


    def get_score(self, sentence1 : str, sentence2 : str):
        model = SentenceTransformer('eladogruyol/pubmedbert-base-embeddings-base-sentence-transformer')


        embeddings1 = model.encode(sentence1)
        embeddings2 = model.encode(sentence2)

        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        score_tensor = cosine_scores[0].item()
        score_float = float("{:.4f}".format(a))
        return score_float
