import re
from typing import Optional

REGEX_YOUTUBE_URL_VALIDATION = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
REGEX_EXTRACT_VIDEO_ID = r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/]+/[^/]+/|(?:v|e|embed|watch|shorts)/|.*[?&]v=)|youtu\.be/)([a-zA-Z0-9_-]{11})"

EMBED_URL_VIDEO_PATTERN = "https://www.youtube.com/embed"


def calculate_offset(page: int, items_per_page: int) -> int:
    return items_per_page * (page - 1)


def calculate_total_of_pages(total_of_items: int, items_per_page: int) -> int:
    return (total_of_items + items_per_page - 1) // items_per_page


def youtube_url_is_valid(link: str) -> bool:
    valid_url = re.fullmatch(REGEX_YOUTUBE_URL_VALIDATION, link) is not None
    return valid_url


def extract_video_id_from_url(url: str) -> Optional[str]:
    matched_pattern = re.search(REGEX_EXTRACT_VIDEO_ID, url)
    return matched_pattern.group(1) if matched_pattern else None


def build_embed_url(video_id: str) -> str:
    return f"{EMBED_URL_VIDEO_PATTERN}/{video_id}"


def get_previous_page(current_page: int) -> int | None:
    if current_page == 1:
        return None
    return current_page - 1


def get_next_page(current_page: int, total_of_pages: int) -> int | None:
    if current_page < total_of_pages:
        return current_page + 1

    return None
