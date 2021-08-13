from django.urls import path, include
from store.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', store_main, name='store_main'),
    path('subpage/', subpage, name="subpage"),
    path('widget/<int:id>', detailpage, name="detailpage"),
    path('mypage/', mypage, name="mypage"),
    path('widget/like', like, name="like"),
    path('widget/comment/write/', comment_write, name="comment_write"),
    path('widget/download/', make_download, name="widget_download"),
    path('widget/show/reply/', reply_comment, name="reply_comment"),
    path('widget/reply/write/', make_reply, name="make_reply"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)