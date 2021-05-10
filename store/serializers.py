from rest_framework import serializers
from store.models import Order, OrderedService, Quote


class OrderedServiceSerializer(serializers.ModelSerializer):
    """ Serializer for OrderedService model """

    service = serializers.SlugRelatedField(
        read_only=True,
        slug_field='service'
    )
    get_price_for_ordered_batch = serializers.CharField()

    class Meta:
        model = OrderedService
        fields = '__all__'
        extra_fields = ['get_price_for_ordered_batch']


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model """

    payment_method = serializers.CharField(source='get_payment_method_display')
    type = serializers.CharField(source='get_type_display')
    status = serializers.CharField(source='get_status_display')
    get_total = serializers.CharField()
    orderedservice_set = OrderedServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_fields = ['orderedservice_set', 'get_total']


class QuoteSerializer(serializers.ModelSerializer):
    """ Serializer for Quote model """

    desc = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = Quote
        fields = ['desc']
