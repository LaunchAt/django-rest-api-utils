from rest_framework.pagination import CursorPagination as BaseCursorPagination


class CursorPagination(BaseCursorPagination):
    cursor_query_param = 'cursor'
    page_size = 10
    ordering = None
    page_size_query_param = 'page_size'
    max_page_size = 100
    offset_cutoff = 100000
