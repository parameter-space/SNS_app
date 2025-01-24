from rest_framework.pagination import PageNumberPagination
from django.conf import settings 
from rest_framework.response import Response
from collections import OrderedDict 


class CustomPagination(PageNumberPagination):
    default_page_size = 10

    """paginate 함수 오버라이딩해서 사용"""
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get('page_size', self.default_page_size)
        if page_size == 'all':
            self.page_size = len(queryset)
        else:
            try:
                self.page_size = int(page_size)
            except ValueError:
                self.page_size = self.default_page_size


        return super().paginate_queryset(queryset, request, view) # 내 로직 다 돌아가고 부모 로직도 돌린걸 반환환다.
# 상속받은 자식 클래스에서 self.page_size를 설정했기 때문에 부모 클래스의 메서드를 돌려도 page_size가 새로 설정되지 않는다.

    def get_paginated_response(self, data): # 출력형식을 바꾸는 메서드
        """previous page number 및 next page number 오류 catch"""
        try:
            previous_page_number = self.page.previous_page_number()
        except:
            previous_page_number = None

        try:
            next_page_number = self.page.next_page_number()
        except:
            next_page_number = None

        return Response(
            OrderedDict([ 
                ('results', data),
                ('count', len(data)),
                ('total_count', self.page.paginator.count),
                ('Curent_page_number', self.page.number),
                ('next', self.get_next_link()),
                ('next_page_number', next_page_number),
                ('previous', self.get_previous_link()),
                ('previous_page_number', previous_page_number)
            ])
        )