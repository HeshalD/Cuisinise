import spacy

nlp = spacy.load("en_core_web_md")

# Test semantic similarity
word1 = nlp("bell pepper")
word2 = nlp("capsicum")

similarity = word1.similarity(word2)
print(f"Similarity between '{word1}' and '{word2}': {similarity:.2f}")
