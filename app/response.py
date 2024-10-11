from abc import abstractmethod, ABC

from app.use_case import build_embed_url


class Response(ABC):
    @abstractmethod
    def get_response():
        pass


class GetAllVideosResponse(Response):
    def __init__(
        self,
        items: list[dict[str, str]],
        items_per_page: int,
        total_of_pages: int,
        page: int,
        prev_page: int | None,
        next_page: int | None,
    ):
        self.items = items
        self.items_per_page = items_per_page
        self.total_of_pages = total_of_pages
        self.page = page
        self.prev_page = prev_page
        self.next_page = next_page

    def get_response(self):
        return {
            "items": [
                {
                    "id": media.get("id"),
                    "title": media.get("title"),
                    "url": media.get("url"),
                }
                for media in self.items
            ],
            "itemsPerPage": self.items_per_page,
            "totalOfPages": self.total_of_pages,
            "page": self.page,
            "prevPage": self.prev_page,
            "nextPage": self.next_page,
        }
