import random
from datetime import date, timedelta, datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Sorovnoma


# Create your views here.
def index(request, id):
    sorovnoma = get_object_or_404(Sorovnoma, id=id)
    total_votes = sorovnoma.number_of_votes
    data = []
    data_colors = []
    colors = ["#1f77b4", "#ff7f0e", " #ffbb78", "#d62728", "#98df8a", "#bcbd22", "#f7b6d2"]
    for i in sorovnoma.variants.all():
        random.shuffle(colors)
        if colors[0] in data_colors:
            random.shuffle(colors)
        data.append({
            'name': i.name,
            "number": i.number_votes,
            "percent": round(i.number_votes * 100 / total_votes, 2),
            "color": colors[0]
        })
        data_colors.append(colors[0])
    context = {
        'total_votes': total_votes,
        "variant": data
    }
    return render(request, "index.html", context)


def statistic(request, id):
    sorovnoma = get_object_or_404(Sorovnoma, id=id)
    total_votes = sorovnoma.number_of_votes
    data = []
    for i in sorovnoma.variants.all():
        data.append({
            'name': i.name,
            "number": i.number_votes,
            "percent": round(i.number_votes * 100 / total_votes, 2)
        })
    context = {
        'total_votes': total_votes,
        "variant": data
    }
    return JsonResponse(context, status=200)


class CronJob(APIView):
    def get(self, request):
        today = date.today()
        # real_date = today + timedelta(days=int(deadline))
        real_datetime = datetime.combine(today, datetime.min.time())
        print(today)
        sorovnomas = Sorovnoma.objects.filter(is_active=True, deadline__lt=today)
        for sorovnoma in sorovnomas:
            sorovnoma.is_active = False
            sorovnoma.save()
            print("allll")
        return Response({"msg": "Success"})
