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

# experimento/views.py

import json

# @csrf_exempt
@csrf_exempt  # Remove this in production if using CSRF protection
def save_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        print('save_response', data)

        trial_id = data.get('trial_id')  # This can be used as trial_number
        response = data.get('response')
        reaction_time = data.get('reaction_time')
        stimulus = data.get('stimulus')  # New data to create a trial
        block_id = 1 # data.get('block_id')  # Assuming you send the block ID in the request

        try:
            # Retrieve the Block instance using the provided block_id
            block = Block.objects.get(id=block_id)

            # Create a new Trial object with the Block instance
            trial = Trial(
                block=block,  # Assign the Block instance here
                trial_id=trial_id,
                stimulus=stimulus,
                response=response,
                correct=False,  # Default value, will set based on logic below
                reaction_time=reaction_time
            )
            
            # Implement your logic to determine if the response is correct
            d_value = stimulus[0]  # Example extraction from stimulus
            prom_fijo = 50  # Define your comparison value

            # if (response == '<' and d_value < prom_fijo) or (response == '>' and d_value > prom_fijo):
                # trial.correct = True
            
            # Save the trial to the database
            trial.save()
            return JsonResponse({'status': 'success', 'trial_id': trial.id})  # Optionally return the new trial ID
        except Block.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Block not found'}, status=404)
        except Exception as e:
            print(f"Error creating trial: {e}")
            return JsonResponse({'status': 'fail', 'message': 'Error creating trial'}, status=500)

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


def finish_experiment(request, session_id):
    session = ExperimentSession.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return render(request, 'experimento/finish_experiment.html')
