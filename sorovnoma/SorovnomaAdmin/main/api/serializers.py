from rest_framework import serializers

from main.models import Sorovnoma, RequiredChannel, Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'name', 'number_votes']
        # fields = '__all__'


class SorovnomaSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    class Meta:
        model = Sorovnoma
        fields = ['id', 'image', 'variants', 'description', 'number_of_votes', "deadline", "is_active"]
        # depth = 1


class RequiredChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredChannel
        # fields = ['id', 'address', 'name']
        fields = '__all__'
