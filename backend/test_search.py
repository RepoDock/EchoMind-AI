from services.search_service import SearchService

service = SearchService()

service.add_document(
    1,
    """
    Database Management System

    Normalization

    BCNF

    SQL
    """
)

service.add_document(
    2,
    """
    Machine Learning

    Deep Learning

    CNN

    AI
    """
)

results = service.search(
    "Normalization Notes"
)

print(results)