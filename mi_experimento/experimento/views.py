# experimento/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ExperimentSession, Block, Trial
import numpy as np
import random
from django.utils import timezone
from experimento.utils import generate_mean_list
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ExperimentResponse  # Asegúrate de tener un modelo adecuado para guardar las respuestas

# experimento/views.py

import json

def save_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        trial_id = data.get('trial_id')
        response = data.get('response')
        reaction_time = data.get('reaction_time')
        
        try:
            trial = Trial.objects.get(id=trial_id)
            trial.response = response
            trial.reaction_time = reaction_time
            # Aquí puedes implementar la lógica para determinar si la respuesta es correcta
            # Por simplicidad, supongamos que d_value ya está almacenado
            d_value = int(trial.stimulus.split(',')[0])  # Ajusta según tu lógica
            prom_fijo = 50  # Ajusta según tu lógica
            if (response == '<' and d_value < prom_fijo) or (response == '>' and d_value > prom_fijo):
                trial.correct = True
            else:
                trial.correct = False
            trial.save()
            return JsonResponse({'status': 'success'})
        except Trial.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Trial not found'}, status=404)
    return JsonResponse({'status': 'fail'}, status=400)

def index(request):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        session = ExperimentSession.objects.create(participant_id=participant_id)
        return redirect('start_experiment', session_id=session.id)
    return render(request, 'experimento/index.html')

def start_experiment(request, session_id):
    session = ExperimentSession.objects.get(id=session_id)
    return render(request, 'experimento/start_experiment.html', {'session_id': session.id})

def run_block(request, session_id, block_number):
    session = ExperimentSession.objects.get(id=session_id)
    block = Block.objects.create(session=session, block_number=block_number)
    
    # Generar diseño del bloque
    total_trials = 10
    d = [41,44,46,48,49,51,52,54,56,59]
    prom_fijo = 50
    std = 15
    large = 8
    
    trials_data = []
    for trial_num in range(total_trials):
        d1 = random.randint(0, len(d)-1)
        numeros = generate_mean_list(d[d1], std, large)
        numeros = [int(n) for n in numeros]
        trials_data.append({
            'trial_number': trial_num + 1,
            'stimulus': numeros,
            'd1': d1,
            'd_value': d[d1],
            'prom_fijo': prom_fijo
        })
    
    return render(request, 'experimento/run_block.html', {
        'session_id': session.id,
        'block_id': block.id,
        'trials': trials_data,
    })

@csrf_exempt
def save_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        trial_id = data.get('trial_id')
        response = data.get('response')
        reaction_time = data.get('reaction_time')

        # Guarda la respuesta en la base de datos
        ExperimentResponse.objects.create(
            trial_id=trial_id,
            response=response,
            reaction_time=reaction_time
        )

        # Envía una respuesta JSON de confirmación
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

def finish_experiment(request, session_id):
    session = ExperimentSession.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return render(request, 'experimento/finish_experiment.html')
