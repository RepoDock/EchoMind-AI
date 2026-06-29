from services.indexing_service import IndexingService

service = IndexingService()

result = service.index_folder("sample-data")

print(result)