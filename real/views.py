from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Realbar
import pusher
from real.serializers import BarcodeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'first':
        barcode_list = Realbar.objects.order_by('create_date')
    else:  # recent
        barcode_list = Realbar.objects.order_by('-create_date')

    # 조회
    if kw:
        barcode_list = barcode_list.filter(
            Q(id__icontains=kw) |  # Id검색
            Q(barcode__icontains=kw) |  # 바코드검색
            Q(create_date__icontains=kw) # 생성일시검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(barcode_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'barcode_list': page_obj, 'page': page, 'kw': kw, 'so': so}

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
