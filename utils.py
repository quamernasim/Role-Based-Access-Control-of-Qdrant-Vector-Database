import jwt
import pandas as pd
from tqdm.notebook import tqdm

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Batch

def generate_embeddings_from_fastext_model(docs, embed_model):
    '''
    Generate embeddings for the documents using the FastText model
    
    Args:
    docs: List of documents
    embed_model: FastText model
    
    Returns:
    df: Dataframe with the documents, embeddings, metadata and payload
    '''

    # convert the documents to a dataframe
    # This dataframe will be used to create the embeddings
    # And later will be used to update the Qdrant Vector Database
    data = []
    for doc in tqdm(docs):
        # Get the page content and metadata for each chunk
        # Meta data contains chunk source or file name
        row_data = {
            "page_content": doc.page_content,
            "metadata": doc.metadata
        }
        data.append(row_data)

    df = pd.DataFrame(data)

    # Replace the new line characters with space
    df['page_content'] = df['page_content'].replace('\\n', ' ', regex=True)

    # Create a unique id for each document.
    # This id will be used to update the Qdrant Vector Database
    df['id'] = range(1, len(df) + 1)

    # Create a payload column in the dataframe
    # This payload column includes the page content and metadata
    # This payload will be used when LLM needs to answer a query
    df['payload'] = df[['page_content', 'metadata']].to_dict(orient='records')

    # Create embeddings for each chunk
    # This embeddings will be used when doing a similarity search with the user query
    df['embeddings'] = df['page_content'].apply(lambda x: (embed_model.get_sentence_vector(x)).tolist())

    return df


def generate_jwt(api, payload):
    '''
    This function generates a JWT token using the payload and the API key

    Args:
    api: API key
    payload: Payload to be encoded in the JWT token. It contains the access rights

    Returns:
    encoded_jwt: JWT token
    '''
    encoded_jwt = jwt.encode(payload, api, algorithm='HS256')
    return encoded_jwt


def create_new_collection(url, jwt, collection_name, df, vector_size, batch_size, delete_prev = False, create_from_scratch = False):

    '''
    This function creates a new collection in Qdrant Vector Database
    and updates the collection with the embeddings

    It starts by creating a connection to the Qdrant Vector Database running using the docker
    Then it deletes the collection if it already exists
    Then it creates a new collection with the specified collection name and vector size
    Then it updates the collection with the embeddings
    Finally, it closes the connection to the Qdrant Vector Database and returns the client object

    Args:
    url: URL of the Qdrant Vector Database
    jwt: JWT token
    collection_name: Name of the collection
    df: Dataframe with the documents, embeddings, metadata and payload

    Returns:
    client: QdrantClient object
    '''

    # Create a QdrantClient object
    # client = QdrantClient('https://localhost:6333')
    client = QdrantClient(url=url, api_key = jwt)

    # delete the collection if it already exists
    # remove or comment this line if you want to keep the existing collection
    # and want to use the existing collection to update new points
    if delete_prev:
        client.delete_collection(collection_name=collection_name)

    # Create a fresh collection in Qdrant
    # remove or comment this line if you do not want to create a new collection
    if create_from_scratch:
        client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    # Update the Qdrant Vector Database with the embeddings
    # We are updating the embeddings in batches
    # Since the data is large, we will only update the first batch of size 4000
    client.upsert(
    collection_name=collection_name,
    points=Batch(
        ids=df['id'].to_list()[:batch_size],
        payloads=df['payload'][:batch_size],
        vectors=df['embeddings'].to_list()[:batch_size],
    ),
    )

    # Close the QdrantClient
    client.close()

    print(f"Collection {collection_name} created and updated with the embeddings")