
import django_filters
from room.models import Hotel, Reserved


class HotelFilter(django_filters.FilterSet):
    '''
        filter classs by name of hotel and county rating and room_type
    '''
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    county = django_filters.CharFilter(field_name='county__name', lookup_expr='iexact')
    rating = django_filters.NumericRangeFilter(field_name='rating')
    room_type = django_filters.CharFilter(field_name='room__room_type', lookup_expr='iexact')

    class Meta:
        model = Hotel
        fields = ('name', 'county', 'rating', 'room_type')


class ReservedFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='from_date', lookup_expr='gt')
    to_date = django_filters.DateFilter(field_name='to_date', lookup_expr='lt')

    class Meta:
        model = Reserved
        fields = ('from_date', 'to_date')