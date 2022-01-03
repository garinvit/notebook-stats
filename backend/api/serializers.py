from rest_framework import serializers
from miner.models import Miner, Stats
from app.utils import query_debugger  # noqa


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'
        extra_kwargs = {'miner': {'required': True}}


class MinerSerializer(serializers.ModelSerializer):
    # stats_set = StatsSerializer(many=True, required=False)
    class Meta:
        model = Miner
        fields = '__all__'