from django.db.models.expressions import F
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .finance import crawl_finance
from .models import Layout
from account.views import get_user_inst
import json


def finance_view(request):
  return render(request, 'finance.html')


def get_finance(request):
  priceList = crawl_finance(request.GET)
  return_str = ""
  for item in priceList:
    return_str += (item + "/")
  return HttpResponse(return_str)

  
def stickynote_view(request):
  return render(request, 'stickynote.html')


def dday_view(request):
  return render(request, 'dday.html')


def get_dday(request):
  return HttpResponse()


def searching_view(request):
  return render(request, 'searching.html')


def todo_view(request):
  return render(request, 'todo.html')

def github_view(request):
  return render(request, 'github.html')

def webtoon_view(request):
  return render(request, 'webtoon.html')


def layout_add(request):
  user = get_user_inst(request)
  Layout.objects.create(creater=user, owner=user, data="[]", from_store = False)
  return redirect('test')

def apply_layout(request, pk):
  user = get_user_inst(request)
  qs = Layout.objects.filter(owner=user, seq=pk, is_applied=False)
  applied_qs = Layout.objects.filter(owner=user, is_applied=True)

  if len(qs) == 1 and len(applied_qs) == 1:
    applied_qs.update(is_applied=False)
    qs.update(is_applied=True)
    return redirect('home')
  return redirect('home')  

def layout_delete(request, pk):
  user = get_user_inst(request)
  qs = Layout.objects.filter(owner = user, seq = pk)
  if len(qs) == 1:
    qs.delete()
    return redirect('test')


def layout_clone(request, pk):
  user = get_user_inst(request)
  qs = Layout.objects.filter(owner = user, seq = pk)
  if is_distinct_QS(qs):
    Layout.objects.create(creater = user, owner = user, from_store = False, data = qs[0].data, is_applied = False)
    return redirect('test')
    

def insert_dummy_layout(request, apply):
  user = get_user_inst(request)
  Layout.objects.create(owner=user, creater=user, from_store=False, is_applied=apply,data='[{"type": "finance","posX": "300px","posY": "500px","contents": {"items": ["애플", "아마존", "구글", "마이크로소프트"]}},{"type": "d-day","posX": "300px","posY": "100px","content": {"items": ["헤커톤:2021-08-15", "개강:2021-09-01", "한살 더먹음:2022-01-01"]}},{"type": "searching","posX": "700px","posY": "500px","content": {"engine": "naver", "width": "500px", "height": "70px"}},{"type": "stickynote","posX": "700px","posY": "100px","contents": {"title": "다이어트 계획", "memo": "없음"}}]')
  return True


def view_list(request):
  user = get_user_inst(request)
  layout_list = Layout.objects.filter(owner=user, widget_type='layout_widget')
  print("LAYOUT LIST")
  print(layout_list)
  return layout_list

def get_applied_layout(request):
  user = get_user_inst(request)
  qs = Layout.objects.filter(owner=user, is_applied=True)
  json = "[]"
  if is_distinct_QS(qs):
    json = qs[0].data
  return HttpResponse(json)
  

def is_distinct_QS(QS):
  if len(QS) == 1:
    return True
  return False


# LAYOUT = '[{"type": "finance","contents": {"width": "340px", "posX": "300px","posY": "500px","items": ["삼성전자", "네이버", "카카오", "JYP Ent"]}},{"type": "stickynote","contents": {"width": "160px", "height": "160px", "posX": "700px","posY": "500px", "title": "Sticky Note", "memo": "내용을 작성하세요!"}},{"type": "searching","contents": {"width": "500px", "height": "70px", "posX": "100px","posY": "100px", "bgColor": "#ee531e", "engine": "google"}},{"type": "searching","contents": {"width": "500px", "height": "70px", "posX": "700px","posY": "100px", "bgColor": "#14ea18", "engine": "naver"}},{"type": "dday","posX": "200px","posY": "100px","contents": {"items": ["헤커톤:2021-08-15", "개강:2021-09-01", "한살 더먹음:2022-01-01"]}}]'


def insert_dummy_layout(request, apply):
  user = get_user_inst(request)
  # Layout.objects.filter(owner=user).delete()
  # Layout.objects.create(owner=user, creater=user, from_store=False, is_applied=apply,data=LAYOUT)
  return True

def book_view(request):
  return render(request, 'book.html')

def timer_view(request):
  return render(request, 'timer.html')


def update_main_bgcolor(request):
  hexColor = request.GET['hexColor']
  return HttpResponse(True)


def save_layout(request):
  layout_JSON = request.GET['layoutJSON']
  user = get_user_inst(request)
  Layout.objects.filter(owner=user, is_applied=True).update(data=layout_JSON)
  return HttpResponse(True)


def get_download_widget(request):
  user = get_user_inst(request)
  QS = Layout.objects.filter(owner=user, is_widget=True, from_store=True)
  return QS


def widget_append(request):
  widget_seq = request.GET['widgetSEQ']
  user = get_user_inst(request)
  QS = Layout.objects.filter(owner=user, is_applied=True)
  origin = json.loads(QS[0].data)
  new_widget_QS = Layout.objects.filter(owner=user, seq=widget_seq)
  if len(new_widget_QS) == 1:
    new_list = json.loads(new_widget_QS[0].data)
    origin += new_list
  QS.update(data=json.dumps(origin))
  return HttpResponse(True)
  

def weather(request):
  return render(request, 'weather.html')