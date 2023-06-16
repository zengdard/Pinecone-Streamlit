import streamlit as st
import time

import openai

openai.api_key  = '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'
MODEL = "text-embedding-ada-002"

# Instanciez le client Pinecone
pinecone.init(api_key="adc9813f-f17f-49a6-befb-764a06fdad9a", environment="us-west4-gcp-free")
index_name = "stendhalgpt"
index = pinecone.Index(index_name)

def search(query, top_k=5):
    response = openai.Embedding.create(
        input=query,
        model=MODEL
    )

    embedding = response['data'][0]['embedding']
    try : 
        results = index.query(queries=[embedding], top_k=top_k, include_metadata=True, namespace='FR')
    except: 
            try:
                 results = index.query(queries=[embedding], top_k=top_k, include_metadata=True, namespace='FR')
            except:
                 pass
            results = {}
    return results

st.title("StendhalGPT SOURCES (BETA)")
st.caption('StendhalGPT se veut neutre dans ses résultats proposés.')
st.info("Notre base d'informations s'améliore de jour en jour !")
# Input du texte
user_input = st.text_area("Tapez votre texte ici")

if user_input:
    # Ici, vous devez convertir votre texte en vecteur, en utilisant le même processus que vous avez utilisé pour générer les vecteurs d'origine.
    with st.spinner('Recherche en cours...'):
        # Effectuez la recherche
        results = search(user_input)
        time.sleep(3)
    if results == {}:
         st.warning('Aucun résultat trouvé, ou problème lors de la connexion, veuillez réessayer.')
         st.stop()
    ids = []
    # Créez des "onglets" pour chaque résultat
    for i, result in enumerate(results['results'][0]['matches']):
        # Si l'ID n'a pas déjà été traité, affichez-le
          if result['metadata']['titre'] not in ids:
            ids.append(result['metadata']['titre'])
            with st.expander(f"Résultats :", expanded=True):
                st.caption(f"Score de similarité: {result['score']}")
                st.markdown(f"## Titre: {result['metadata']['titre']}")
                st.markdown(f"<br>**Extrait:** {result['metadata']['text']}", unsafe_allow_html=True)
                st.markdown(f'<br>**Site:** <a href="http://{result["metadata"]["site"]}" target="_blank">{result["metadata"]["site"]}</a>', unsafe_allow_html=True)
                st.markdown(f'<br><a href="{result["metadata"]["url"]}" target="_blank">{result["metadata"]["url"]}</a>', unsafe_allow_html=True)
