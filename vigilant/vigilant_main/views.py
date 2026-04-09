from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

import json

from . import models
#
#
#
@login_required(login_url='/login')
def main(request):
    data = {
        "connections": models.connection.objects.all()
    }

    rend = render(request, "main.html", data)
    resp = HttpResponse(rend)
    return resp
#
#
#
@login_required(login_url='/login')
def connection(request):
    connection_id = request.GET.get("id")
    data = dict()
    try:
        connection = models.connection.objects.get(id=connection_id)
        data = {
            "fields": connection.fields.strip().split(","),
            "entries": list(models.log_entry.objects.filter(connection=connection).order_by("-created").values_list("content", flat=True)).limit(100)
        }

    except Exception as ex:
        print(ex)

    resp = JsonResponse(data, safe=False)
    return resp