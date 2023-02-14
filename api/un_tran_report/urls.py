from django.urls import include, path
from api.un_tran_report.views import UserInfoViewAPI
from rest_framework.routers import DefaultRouter

# userinfo = UserInfoViewAPI.as_view({"get": "retrieve"})
# urlpatterns = [
#     path('userinfo/<str:pk>/', userinfo),
# ]

urlpatterns = [
   path('api/<str:pk>', UserInfoViewAPI.as_view()),
   #path(r'api', UserInfoViewAPI.as_view()),
]
