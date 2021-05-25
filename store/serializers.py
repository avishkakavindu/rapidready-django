from rest_framework import serializers
from store.models import Order, OrderedService, Quote, CartItem, Service, Cart


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


class CartItemSerializer(serializers.ModelSerializer):
    """ Serializer for Cart Item model """

    id = serializers.IntegerField(read_only=True)
    service = serializers.PrimaryKeyRelatedField(required=True, queryset=Service.objects.all())
    quantity = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = CartItem
        fields = ['id', 'service', 'quantity', 'get_total_for_item']


class CartSerializer(serializers.ModelSerializer):
    """ Serializer for Cart model """

    cartitem_set = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'cartitem_set', 'get_cart_total']
        
    def update(self, instance, validated_data):
        items = validated_data.pop('cartitem_set')

        for item in items:
            if 'id' in item.keys():
                if CartItem.objects.filter(cart=instance.id, id=item['id']).exists():
                    cart_item = CartItem.objects.get(id=item['id'])
                    cart_item.quantity = item.get('quantity', cart_item.quantity)
                    cart_item.save()
            elif 'service' in item.keys():
                try:
                    cart_item = CartItem.objects.get(cart=instance.id, service=item['service'])
                except:
                    cart_item = CartItem.objects.create(cart=instance, service=item['service'])

                cart_item.quantity = item.get('quantity', cart_item.quantity)
                cart_item.save()
        return instance




