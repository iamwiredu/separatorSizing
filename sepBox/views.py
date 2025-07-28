from django.shortcuts import render, redirect, get_object_or_404
from .models import VerticalSeparatorDesign, HorizontalSeparatorDesign
from SeparatorSizing import run_vertical_separator_calc, run_horizontal_separator_calc

def calc_separator(request):
    if request.method == 'POST':
        separator_type = request.POST.get('separator_type', 'vertical')

        data = {
            'name': request.POST['name'],
            'Wg': float(request.POST['Wg']),
            'Wl': float(request.POST['Wl']),
            'Pg': float(request.POST['Pg']),
            'Pl': float(request.POST['Pl']),
            'Ug': float(request.POST['Ug']),
            'dp': float(request.POST['dp']),
            'velocity_factor': float(request.POST['velocity_factor']),
            'holdup_time': int(request.POST['holdup_time']),
            'surge_factor': float(request.POST['surge_factor']),
            'pressure': float(request.POST['pressure']),
            'mist_eliminator_ring': float(request.POST['mist_eliminator_ring']),
        }

        # Only for vertical
        if separator_type == 'vertical':
            data['dn'] = float(request.POST['dn'])
            data['inlet_diverter'] = request.POST.get('inlet_diverter') == 'on'
            data['mist_eliminator_present'] = request.POST.get('mist_eliminator_present') == 'on'

            results = run_vertical_separator_calc(data)
            design = VerticalSeparatorDesign.objects.create(**data, **results)
            return render(request, 'result.html', {'design': design, 'type': 'vertical'})

        else:
            data['mist_eliminator_present'] = request.POST.get('mist_eliminator_present') == 'on'
            data['L_D_ratio'] = float(request.POST['L_D_ratio'])
            results = run_horizontal_separator_calc(data)
            design = HorizontalSeparatorDesign.objects.create(**data, **results)
            return render(request, 'result.html', {'design': design, 'type': 'horizontal'})

    return render(request, 'main.html')
