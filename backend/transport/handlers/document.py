import os
import tempfile
from typing import Annotated
from litestar import Request, post, get
from litestar.enums import RequestEncodingType
from litestar.datastructures import UploadFile
from litestar.response import Response
from litestar.params import Body
from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from aiologger import Logger

from repositories.repositories import Repositories
from transport.schemas.response import (
    NewResponseWithData,
    NewResponseWithMessageERROR,
    NewJSONResponseOK,
)


def insert_document(route: str):
    @post(route, max_upload_size=10_000_000, sync_to_thred=False)
    async def handler(
        repositories: Repositories, 
        logger: Logger, 
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        request: Request
    ) -> Response:
        try:
            agent_id = request.query_params.get("agent_id")
            if not agent_id:
                return NewResponseWithMessageERROR(
                    status_code=400, message="Agent ID is required"
                )
            
            if not data:
                return NewResponseWithMessageERROR(
                    status_code=400, message="No file uploaded"
                )
                
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file_path = temp_file.name
                content = await data.read()
                temp_file.write(content)
            
            try:
                file_extension = os.path.splitext(data.filename)[1].lower()
                
                if file_extension == '.pdf':
                    loader = PyPDFLoader(temp_file_path)
                elif file_extension == '.md':
                    loader = UnstructuredMarkdownLoader(temp_file_path)
                else:
                    loader = TextLoader(temp_file_path)
                
                documents = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=256,
                    chunk_overlap=64,
                )
                chunks = text_splitter.split_documents(documents)
                
                for chunk in chunks:
                    repositories.document.insert_document(chunk.page_content, agent_id)
                
                return NewJSONResponseOK(status_code=201)
                
            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Server error"
            )
        
    return handler


def search_similar_documents(route: str):
    @get(route, sync_to_thread=False)
    def handler(
        repositories: Repositories, logger: Logger, request: Request
    ) -> Response:
        try:
            query = request.query_params.get("query")
            agent_id = request.query_params.get("agent_id")
            top_k = int(request.query_params.get("top_k", 5))

            if not query:
                return NewResponseWithMessageERROR(
                    status_code=400, message="Параметр 'query' обязателен"
                )

            results = repositories.document.search_similar(query, agent_id, top_k)
            return NewResponseWithData(status_code=200, data=results)

        except Exception as e:
            logger.error(f"Ошибка поиска документов: {e}")
            return NewResponseWithMessageERROR(
                status_code=500, message="Ошибка сервера"
            )

    return handler
