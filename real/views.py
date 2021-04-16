from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Realbar
import pusher
from real.serializers import BarcodeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


def index(request):
    barcode_list = Realbar.objects.order_by('-create_date')
    context = {'barcode_list': barcode_list}

    return render(request, 'real/barcode_list.html', context)


@csrf_exempt
def barcode_list(request):
    global bdata
    if request.method == 'GET':
        query_set = Realbar.objects.all()
        serializer = BarcodeSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BarcodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()       # DB저장
            sendPush(serializer.data)
            # print("비데이터의 형식 : ", type(serializer.data))
            # print("비데이터 : ", serializer.data)
            # print("아이디 : ", serializer.data["id"])
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def sendPush(data):
    pusher_client = pusher.Pusher(
        app_id='1187992',
        key='af1394a6d38f4e31ac54',
        secret='92529e0c8378dd72a42f',
        cluster='ap3',
        ssl=True
        )
    pusher_client.trigger('my-channel', 'my-event', data)
