from django.urls import path, include

from main import views

urlpatterns = [
    path('/api/v1/', include(('main.api.urls', 'api'))),
    path('chart/<int:id>/', views.index, name='index'),
    path('statistic/<int:id>/', views.statistic, name='statistic'),

]
