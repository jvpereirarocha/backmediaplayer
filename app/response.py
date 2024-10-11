from abc import abstractmethod, ABC

from app.use_case import build_embed_url


class Response(ABC):
    @abstractmethod
    def get_response():
        pass


class GetAllVideosResponse(Response):
    def __init__(self, items: list[dict[str, str]], items_per_page: int, page: int, prev_page: int | None, next_page: int | None):
        self.items = items
        self.items_per_page = items_per_page
        self.page = page
        self.prev_page = prev_page
        self.next_page = next_page

    def get_response(self):
        return {
            "items": [
                {"id": media.get("id"), "title": media.get("title"), "url": media.get("url")}
                for media in self.items
            ],
            "items_per_page": self.items_per_page,
            "page": self.page,
            "prev_page": self.prev_page,
            "next_page": self.next_page,
        }