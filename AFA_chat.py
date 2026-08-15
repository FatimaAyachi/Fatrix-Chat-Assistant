import json
import random
import numpy as np
import nltk
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob

nltk.download('punkt')
nltk.download('wordnet')

# Initialisation du lemmatiseur pour normaliser les mots
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = nltk.word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(w) for w in words if w not in string.punctuation]
    processed_text= " ".join(words)
    return processed_text

try:
    with open("intents.json","r",encoding = "utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["hello", "hi", "hey", "good morning"],
                "responses": ["Hello! How can I help you?"]
            }
        ]
    }
except Exception as e:
    exit()


#Préparation des données d’entraînement
petterns=[]
tags=[]

for intent in data["intents"]:
    for parttern in intent["patterns"]:
        processed_pattern = preprocess_text(parttern)
        petterns.append(processed_pattern)
        tags.append(intent["tag"])

#Dictionnaire pattern → tag
PATTERN_DICT= {}
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        processed= preprocess_text(pattern)
        PATTERN_DICT[processed] = intent["tag"]

#Ce composant sert à transformer le texte (phrases) en vecteurs numériques
vectorized = TfidfVectorizer(ngram_range=(1,2),min_df=1,max_features=2000)

# Apprentissage du vocabulaire et transformation des phrases en vecteurs
X = vectorized.fit_transform(petterns)

#Création du modèle Logistic Regression
# max_iter=1000 : nombre maximum d’itérations pour assurer la convergence
# C=1.0 : paramètre de régularisation (équilibre entre précision et généralisation)
model= LogisticRegression(max_iter=1000 ,C=1.0)

#Entraînement du modèle
# Le modèle apprend la relation entre :
# X : phrases transformées en nombres
# tags : intentions correspondantes
# Après cette étape, le modèle peut prédire l’intention d’un nouveau message
model.fit(X,tags)

#Recherche par similarité (Jaccard)
def analyse_sentiment(text):
    try:
        blod = TextBlob(text)
        polarity = blod.sentiment.polarity

        if polarity > 0.1:
            return "positive"
        elif polarity <-0.1 :
            return "negative"
        else:
            return "neutral"
    except:
        return "neutral"


#fallback

funny_fallback_responces = [
    "😂 حتى أنا ضعت",
    "🤡 هادي صعيبة عليا",
    "😎 هدر بشوية راه ماشي شفرة",
    "🤖 Brain.exe توقف فجأة",
"آش خبارك؟ شنو واقع؟ شكون عيط ليك دابا؟ 😂",
    "واش باغي تضحك ولا نعاونو فشي حاجة؟ 😎",
    "هادي غير ضحكة صغيرة، ما تاخدهاش جد 😜",
    "صافي هاني معاك، سولني على اللي بغيتي 😁",
    "يلاه نضحكو شوية، الدنيا ماشي كلها جدّية! 😂",
]

def find_best_match(user_input):
    user_words = set(preprocess_text(user_input).split())
    best_score = 0
    best_tag = None

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern_words =  set(preprocess_text(pattern).split())
            intersection = len(user_words & pattern_words)
            union = len(user_words | pattern_words)
            if union > 0:
                similarity = intersection / union
                if similarity> best_score:
                    best_score = similarity
                    best_tag = intent["tag"]
    return best_tag,best_score

def chatbot_response(user_input):

    processed_input = preprocess_text(user_input)

    try:
       if not processed_input.strip():
           return "I need bit more than that!"

       # Vérification directe si le message correspond exactement à un pattern connu
       if processed_input in PATTERN_DICT:
            tag = PATTERN_DICT[processed_input]
            for intent in data["intents"]:
                if intent ["tag"] == tag :
                    return random.choice(intent["responses"])

       # Gestion des messages très courts avec similarité (Jaccard)
       if len(processed_input.split())<= 3:
           best_tag, similarity_score = find_best_match(user_input)
           if best_tag and similarity_score > 0.3:
                for intent in data["intents"]:
                    if intent["tag"] == best_tag:
                        return random.choice(intent["responses"])

       # Transformer le texte utilisateur en vecteur numérique avec TF-IDF
       X_test = vectorized.transform([processed_input])
       # Calculer les probabilités de chaque intention avec la régression logistique
       probs= model.predict_proba(X_test)[0]
       # Récupérer l’index de la probabilité la plus élevée
       max_prob_index=np.argmax(probs)
       # Identifier l’intention (tag) la plus probable
       tag = model.classes_[max_prob_index]
       # Obtenir la valeur de la probabilité maximale (confiance du modèle)
       max_prob = probs[max_prob_index]
       # Seuil minimal de confiance pour accepter la prédiction
       threshold = 0.3
       # Analyser le sentiment du message utilisateur (positif, négatif ou neutre)
       sentiment = analyse_sentiment(user_input)

       # Gestion des messages à sentiment négatif
       if sentiment == "negative":
            if tag == "feeling_sad" and max_prob > 0.2:
                for intent in data["intents"]:
                    if intent["tag"] == "feeling_sad":
                         return random.choice(intent["responses"])
            return "I'm sorry you're feeling down. How can i assist you?"

       # Gestion des messages à sentiment positif
       elif sentiment== "positive":
            if max_prob < threshold:
                return "Glad to hear that ! how i can assist your further"
            else:
               return "Glad to hear that ! " + random.choice([resp for intent in data["intents"] if intent["tag"]== tag for resp in intent["responses"]])
        # Fallback si la confiance du modèle est faible
       if max_prob  < threshold:
           best_tag, similarity_score = find_best_match(user_input)
           if best_tag and similarity_score > 0.2:
               for intent in data["intents"]:
                   if intent["tag"] == best_tag:
                       return  random.choice(intent["responses"])

           return random.choice(funny_fallback_responces)
       else:
          for intent in data["intents"]:
              if intent["tag"] ==tag:
                   return random.choice(intent["responses"])
       return random.choice(funny_fallback_responces)

    except Exception as e:
       print(f"Error in chatbot_responce: {e}")

       return "Sorry, an error occurred. Please try again."


print(string.punctuation)






