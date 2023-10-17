from library.extract import Extract as e
from library.transformText import transformer
from library.embedding import Embedding
import tempfile

class PdfService:
    def __init__(self) -> None:
        pass

    def extract_text(pdf):
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf.write(pdf.read())
        temp_pdf.close()

        doc = e.extract_document_by_langchain(temp_pdf.name)
        normalize_doc = e.normalize(doc)
        text = e.splicing(normalize_doc, len(normalize_doc))
        transformed_text = transformer.text_helper(text)
        pieces = e.textSplitter(transformed_text)
        return pieces

    def view_document(docs):
        view_instance = []

        for d in docs:
            view_instance.append({
            "page_content" : d.page_content,
            "metadata" : {'source' : d.metadata['source'], 'pages' : d.metadata['pages']}
        })

        return view_instance

    def create_vectorstore_instances(pieces, source):
        documents = []
        for idx, v in enumerate(pieces):
            documents.append(e.create_doc_instance(v, documents, idx, source))
        return documents

    def create_bm25_instance(docs):
        bm25_instance = []

        for d in docs:
            bm25_instance.append({
            'content' : d.page_content,
            'normalized' : e.tokenizer(d.page_content),
            'source' : d.metadata['soruce'],
            'pages' : d.metadata['pages']
            })

        return bm25_instance

    def add_to_vectorstore(documents, index_name):
        vectorstore = Embedding.get_vectorstore(index_name)
        try:
            vectorstore.add_documents(documents)
        except Exception as e:
            raise e