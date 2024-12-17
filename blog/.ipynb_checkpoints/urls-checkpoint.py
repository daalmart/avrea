# app/urls.py
from django.urls import path
from . import views
from .views import (
    InitView,registro_usuario, test1, testuno, test2, testdos, actividad1, actividad2, actividad3, actividadActivo, 
    actividadTeorica, actividadPragmatica, actividadReflexiva, actividadVisual,actividadKinestesico,
    actividadAuditivo,actividadLE, fin_actividad,
    CustomLoginView, CustomLogoutView,StartEmotionRecognition,actividadAleatoria
)#StopEmotionRecognition


urlpatterns = [
    path('', InitView.as_view(), name='home'),
    path('registro/', registro_usuario, name='registro'),
    path('test1/', test1, name='test1'),
    path('testuno/', testuno, name='testuno'),
    path('guardar_respuestas/', views.guardar_respuestas, name='guardar_respuestas'),
    path('guardar_respuestast2/', views.guardar_respuestast2, name='guardar_respuestast2'),
    path('resultadostest/', views.resultadostest, name='resultadostest'),
    path('test2/', test2, name='test2'),
    path('testdos/', testdos, name='testdos'),
    path('actividad1/', actividad1, name='actividad1'),
    path('actividad2/', actividad2, name='actividad2'),
    path('actividad3/', actividad3, name='actividad3'),
    path('fin_actividad/', views.fin_actividad, name='fin_actividad'),
    path('actividadActivo/', views.actividadActivo, name='actividadActivo'),
    path('actividadTeorica/', views.actividadTeorica, name='actividadTeorica'),
    path('actividadPragmatica/', views.actividadPragmatica, name='actividadPragmatica'),
    path('actividadReflexiva/', views.actividadReflexiva, name='actividadReflexiva'),
    path('actividadVisual/', views.actividadVisual, name='actividadVisual'),
    path('actividadLE/', views.actividadLE, name='actividadLE'),
    path('actividadKinestesico/', views.actividadKinestesico, name='actividadKinestesico'),
    path('actividadAuditivo/', views.actividadAuditivo, name='actividadAuditivo'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('start-emotion-recognition/', StartEmotionRecognition.as_view(), name='start_emotion_recognition'),
    path('actividadAleatoria/', views.actividadAleatoria, name='actividadAleatoria'),
    path('charts/', views.charts, name='charts'),
]
