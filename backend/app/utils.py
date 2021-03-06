from django.http import QueryDict
import json
from rest_framework import parsers
from rest_framework.exceptions import PermissionDenied, NotFound
from django.db import connection, reset_queries
import time
import functools



def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):

        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


backgroundColor = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgb(69,255,1)',
    'rgb(255,152,0)',
    'rgb(0,36,118)',
    'rgb(255,0,0)',
    'rgb(76,0,182)',
    'rgb(128,255,156)',
    'rgb(120,75,186)',
]
borderColor = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgb(108,255,58)',
    'rgb(255,187,56)',
    'rgb(0,81,255)',
    'rgb(255,0,0)',
    'rgb(76,0,182)',
]