from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from . import models

# Create your views here.
def main(request):
    data = {
        "connections": models.connection.objects.all()
    }

    print(data)
    rend = render(request, "main.html", data)
    resp = HttpResponse(rend)
    return resp
#
#
#
def connection(request):
    connection_id = request.GET.get("id")
    data = dict()
    try:
        connection = models.connection.objects.get(id=connection_id)
        data = {
            "fields": connection.fields.strip().split(","),
            "entries": list(models.log_entry.objects.filter(connection=connection).values_list("content", flat=True))
        }

    except Exception as ex:
        print(ex)

    resp = JsonResponse(data, safe=False)
    return resp