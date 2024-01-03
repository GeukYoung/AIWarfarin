from django.shortcuts import render
# from django.http import HttpResponse
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from warfarin.warfarinAI import CalcWarfarin
from warfarin.models import InputData
from collections import Counter
from django.db.models import Count, Min, Max
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create your views here.
def main(request):
    return render(request, 'main_warfarin.html')

def view_result(request):
    if 1:
        gender = float(request.POST.get('gender'))
        age = float(request.POST.get('age'))
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        PTINR_1 = float(request.POST.get('PTINR_1'))
        PTINR_2 = float(request.POST.get('PTINR_2'))
        PTINR_3 = float(request.POST.get('PTINR_3'))
        PTINR_4 = float(request.POST.get('PTINR_4'))
        WFR_1 = float(request.POST.get('WFR_1'))
        WFR_2 = float(request.POST.get('WFR_2'))
        WFR_3 = float(request.POST.get('WFR_3'))
        table_warfarin = CalcWarfarin(gender, age, weight, height, PTINR_1, PTINR_2, PTINR_3, PTINR_4, WFR_1, WFR_2, WFR_3)
        
        input_data = InputData(create_date=datetime.datetime.now(), sex = gender, age = age, bwt = weight, ht = height,
                         PTINR_1 = PTINR_1, PTINR_2 = PTINR_2, PTINR_3 = PTINR_3, PTINR_4 = PTINR_4,
                         WFR_1 = WFR_1, WFR_2 = WFR_2, WFR_3 = WFR_3)
        input_data.save()
        # 1.89 1.98 2.10 2.12
        # 3.5 3.0 3.0
    else:
        table_warfarin = [[2.  , 1.59, 1.36, 1.28, 1.24, 1.21, 1.2 , 1.18, 1.21],
                        [2.02, 1.67, 1.48, 1.43, 1.42, 1.42, 1.43, 1.45, 1.42],
                        [2.04, 1.76, 1.6 , 1.55, 1.55, 1.57, 1.59, 1.61, 1.57],
                        [2.06, 1.87, 1.74, 1.69, 1.68, 1.68, 1.68, 1.69, 1.68],
                        [2.07, 1.98, 1.91, 1.87, 1.85, 1.84, 1.82, 1.81, 1.84],
                        [2.09, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08],
                        [2.1 , 2.17, 2.22, 2.23, 2.23, 2.23, 2.23, 2.24, 2.23],
                        [2.11, 2.25, 2.33, 2.34, 2.32, 2.31, 2.3 , 2.3 , 2.31],
                        [2.13, 2.32, 2.41, 2.4 , 2.38, 2.35, 2.34, 2.33, 2.35],
                        [2.13, 2.37, 2.49, 2.47, 2.43, 2.4 , 2.38, 2.36, 2.4 ],
                        [2.14, 2.42, 2.56, 2.55, 2.51, 2.46, 2.43, 2.4 , 2.46],
                        [2.14, 2.46, 2.63, 2.62, 2.58, 2.53, 2.48, 2.45, 2.53],
                        [2.15, 2.49, 2.69, 2.68, 2.63, 2.58, 2.52, 2.47, 2.58],
                        [2.15, 2.51, 2.73, 2.73, 2.67, 2.61, 2.54, 2.48, 2.61],
                        [2.14, 2.53, 2.76, 2.75, 2.69, 2.61, 2.53, 2.46, 2.61],
                        [2.14, 2.54, 2.78, 2.77, 2.69, 2.59, 2.49, 2.41, 2.59]]
    
    # WFR_min = 0.5
    # WFR_max = 8
    # WFR_increment = 0.5
    # WFR_dose_range = list(np.arange(WFR_min, (WFR_max+0.5), WFR_increment))
    # table_warfarin = np.column_stack((np.transpose(WFR_dose_range),table_warfarin))
    # df = pd.DataFrame(table_warfarin)
    # df.columns = ['Dose','day5','day6','day7','day8','day9','day10','day11','day12','day13',]
    # Manufacturing = [24916, 37941, 29742, 29851, 32490, 30282,
    #             38121, 36885, 33726, 34243, 31050]
    # Sales = [11744, 30000, 16005, 19771, 20185, 24377,
    #             32147, 30912, 29243, 29213, 25663]
    # context = {
    #     'Manufacturing' : Manufacturing,
    #     'Sales' : Sales
    # }
    
    target_PTINR = 2
    diffs = []
    for index, row in enumerate(table_warfarin):
        diff = abs(row[-1] - target_PTINR)
        diffs.append((diff, index))
    # Sort the differences
    diffs.sort()
    # Get the indexes of the rows with the first, second, and third smallest differences
    rank1, rank2, rank3 = diffs[0][1], diffs[1][1], diffs[2][1]
    dosages = ["0.5 mg", "1.0mg", "1.5mg", "2.0mg", "2.5mg", "3.0mg", "3.5mg", "4.0mg", "4.5mg", "5.0mg", "5.5mg", "6.0mg", "6.5mg", "7.0mg", "7.5mg", "8.0mg"]    

    context = {'dose_{}'.format((i + 1)): list(value_PTINR) for i, value_PTINR in enumerate(table_warfarin)}
    # context['table_warfarin'] = table_warfarin
    # context['dosages'] = ["0.5 mg", "1.0mg", "1.5mg", "2.0mg", "2.5mg", "3.0mg", "3.5mg", "4.0mg", "4.5mg", "5.0mg", "5.5mg", "6.0mg", "6.5mg", "7.0mg", "7.5mg", "8.0mg"]
    context['table_warfarin'] = zip(dosages, table_warfarin)
    context['target_warfarin_1'] = rank1
    context['target_warfarin_2'] = rank2
    context['target_warfarin_3'] = rank3
    # context['value_dose'] = range(0.5,8)
    print(context)
    return render(request, 'result_warfarin.html', context)
    # return render(request, 'result_warfarin.html', {'df' : df.to_html(index=False,justify='center')})
    #return render(request, 'result_warfarin.html', {'matrix_data': table_warfarin})

#    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


def visitor_view(request):
    interval = request.GET.get('interval', 'daily')

    # Find the earliest and latest create_date in the database
    earliest_date = InputData.objects.aggregate(Min('create_date'))['create_date__min']
    latest_date = InputData.objects.aggregate(Max('create_date'))['create_date__max']

    if not earliest_date or not latest_date:
        # Handle the case where there are no entries
        earliest_date = datetime.now()
        latest_date = datetime.now()

    if interval == 'daily':
        data = (InputData.objects
                        .filter(create_date__range=(earliest_date, latest_date))
                        .annotate(date=TruncDay('create_date'))
                        .values('date')
                        .annotate(count=Count('id'))
                        .order_by('date'))
    elif interval == 'weekly':
        data = (InputData.objects
                        .filter(create_date__range=(earliest_date, latest_date))
                        .annotate(date=TruncWeek('create_date'))
                        .values('date')
                        .annotate(count=Count('id'))
                        .order_by('date'))
    else:  # Default to daily
        data = (InputData.objects
                        .filter(create_date__range=(earliest_date, latest_date))
                        .annotate(date=TruncMonth('create_date'))
                        .values('date')
                        .annotate(count=Count('id'))
                        .order_by('date'))
        
    # Fill in missing dates with zero visitors
    graph_data = {}
    for entry in data:
        graph_data[entry['date'].date()] = entry['count']
    
    full_date_range = [earliest_date.date() + timedelta(days=x) for x in range((latest_date - earliest_date).days + 1)]
    graph_data = [(date, graph_data.get(date, 0)) for date in full_date_range]

    return render(request, 'visitor.html', {'graph_data': graph_data, 'selected_interval': interval})