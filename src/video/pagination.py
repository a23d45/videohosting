from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class VideoPagination(PageNumberPagination):
    """Пагинатор для списка видео"""
    page_size = 6
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'videos': data
        })