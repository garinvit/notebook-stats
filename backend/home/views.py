import random
from django.contrib.auth.models import User
from django import template
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
import json
from garpix_auth.models.access_token import AccessToken

from miner.forms import MinerForm
from miner.models import Miner, Stats

from app.utils import query_debugger, backgroundColor, borderColor
from api.serializers import MinerSerializer


@login_required(login_url="/login/")
@query_debugger
def index(request):
    miners = Miner.objects.filter(owner=request.user).prefetch_related(Prefetch("stats_set", to_attr="stats_all"))
    all_dates = Stats.objects.filter(miner__owner=request.user).values_list("datetime", "speed", "pool_speed", "id")  #.annotate(data_sum=Sum('speed'))#.aggregate(Sum('speed'))
    result = []
    for i, miner in enumerate(miners):
        ser = MinerSerializer(miner)
        new_dict = ser.data
        stats = miner.stats_all
        stats.reverse()
        temp = []
        pool = []
        speed = []
        labels = []
        for x in stats:
            temp.append(x.temperature)
            pool.append(x.pool_speed)
            speed.append(x.speed)
            labels.append(x.datetime.strftime("%m.%d %H:%M"))
        new_dict.update({"labels": labels,
                         "temperature": temp,
                         "pool_speed": pool,
                         "speed": speed,
                         "background": backgroundColor[i],
                         "border": borderColor[i],
                         })
        result.append(new_dict)
    all_dates = list(map(list, all_dates))
    all_dates.reverse()
    sum_labels = []
    sum_hash = []
    sum_pool = []
    for i, values in enumerate(all_dates):
        if i+1 == len(all_dates):
            break
        if values[0] == all_dates[i+1][0]:
            all_dates[i+1][1] += values[1]
            all_dates[i+1][2] += values[2]
            values = None
        else:
            sum_labels.append(values[0].strftime("%m.%d %H:%M"))
            sum_hash.append(round(values[1], 2))
            sum_pool.append(round(values[2], 2))
    context = {'segment': 'index'}
    context["miners"] = json.dumps(result)
    context["labels"] = json.dumps(labels)
    context["sumLabels"] = json.dumps(sum_labels)
    context["sumHash"] = json.dumps(sum_hash)
    context["sumPool"] = json.dumps(sum_pool)
    context["range"] = range(len(result))

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
@query_debugger
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        print(load_template)
        if load_template == 'page-user.html':
            token = AccessToken.objects.get_or_create(user=request.user)
            print(token, request.user)
            context['token'] = token[0]
        if load_template == 'test.html':
            miners = Miner.objects.all().prefetch_related(Prefetch("stats_set", to_attr="stats_all"))
            result = []
            # max_len = 10
            for i, miner in enumerate(miners):
                ser = MinerSerializer(miner)
                new_dict = ser.data
                stats = miner.stats_all
                stats.reverse()
                # if len(stats) <= max_len:
                #     max_len = len(stats)
                temp = []
                pool = []
                speed = []
                labels = []
                # min_labels = stats[0]
                for x in stats:
                    temp.append(x.temperature)
                    pool.append(x.pool_speed)
                    speed.append(x.speed)
                    labels.append(x.datetime.strftime("%m.%d %H:%M"))
                new_dict.update({"labels": labels,
                                 "temperature": temp,
                                 "pool_speed": pool,
                                 "speed": speed,
                                 "background": backgroundColor[i],
                                 "border": borderColor[i],
                                 })
                result.append(new_dict)
            context = {'segment': 'index'}
            context["miners"] = json.dumps(result)
            context["labels"] = json.dumps(labels)
            context["range"] = range(len(result))
        if load_template == 'ind2.html':
            miner = Miner.objects.get(pk=1)  # filter(owner=request.user)
            stats = Stats.objects.filter(miner=miner).order_by("datetime")
            labels = [x.strftime("%m.%d %H:%M") for x in stats.values_list('datetime', flat=True)]
            values = list(stats.values_list('temperature', flat=True))
            values2 = list(stats.values_list('pool_speed', flat=True))
            values3 = list(stats.values_list('speed', flat=True))
            context = {'segment': 'index',
                       "labels": json.dumps(labels),
                       "values": json.dumps(values),
                       "values2": json.dumps(values2),
                       "values3": json.dumps(values3),
                       }
        if load_template == 'edit-miner.html':
            if request.method == 'POST':
                post = request.POST.copy()
                post["owner"] = request.user.id
                form = MinerForm(post, request.FILES, initial={"owner": request.user.id})
                if form.is_valid():
                    miner = form.save()
                    return redirect(f"/")
            else:
                form = MinerForm(initial={"owner": request.user.id})
        if load_template == 'miners.html':
            miners = Miner.objects.filter(owner=request.user)
            context['miners'] = Miner.objects.filter(owner=request.user)

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
