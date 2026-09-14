import chromadb

from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def chunk_text(
    text,
    chunk_size=1000
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


def index_document(
    text,
    document_name
):

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(
        chunks
    ).tolist()

    ids = [
        f"{document_name}_{i}"
        for i in range(len(chunks))
    ]

    try:

        collection.delete(
            where={
                "source": document_name
            }
        )

    except:
        pass

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {
                "source": document_name
            }
            for _ in chunks
        ]
    )


def search_document(
    query,
    top_k=3
):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    documents = results["documents"][0]

    limited_docs = []

    current_size = 0

    max_chars = 5000

    for doc in documents:

        if current_size + len(doc) > max_chars:
            break

        limited_docs.append(
            doc
        )

        current_size += len(doc)

    return limited_docs