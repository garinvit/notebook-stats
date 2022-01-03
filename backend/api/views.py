import datetime

from django.db import models
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from miner.models import Miner, Stats
from app.utils import query_debugger  # noqa
from .serializers import StatsSerializer


def roundTime(dt=None, roundTo=5 * 60):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


class AddStatsView(CreateAPIView):
    model = Stats
    permission_classes = (IsAuthenticated,)
    serializer_class = StatsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # print("data view:", data)
        miner = Miner.objects.filter(owner=request.user).get(miner_worker=data.get("miner_worker"))
        data['miner'] = miner.id
        data['datetime'] = roundTime(dt=datetime.datetime.now(), roundTo=300)
        # print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
