from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from tensorflow.keras.layers import Input
from tensorflow.keras.models import load_model
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import h5py
import subprocess
from django.http import JsonResponse
import json
import os
from django.views import View
from .models import EA_Respuestas
from .models import Emotions_Activities
from deepface import DeepFace
from threading import Thread
from pytz import timezone
from datetime import datetime, timezone
import threading
emotion_data=[]


class EmotionsThread(threading.Thread):
    
    def __init__(self, cap, user, data, name='EmotionsThread'):
        """ constructor, setting initial variables """
        self.cap=cap
        self.data=data
        self.user=user
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)

    def run(self):
        """ main control loop """
        print("%s starts" % (self.getName(),))
        try:
        
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            count = 0
            while not self._stopevent.isSet():
                count += 1
                print("loop %d" % (count,))
                self._stopevent.wait(self._sleepperiod)
                ret, frame = self.cap.read()

                # Convert frame to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Convert grayscale frame to RGB format
                rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

                # Detect faces in the frame
                faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    # Extract the face ROI (Region of Interest)
                    face_roi = rgb_frame[y:y + h, x:x + w]
                    # Perform emotion analysis on the face ROI
                    result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                    # Determine the dominant emotion
                    emotion = result[0]['dominant_emotion']
                    print("Dominant emotion:",emotion)
                    # Guardar la emoción con la marca de tiempo
                    emotion_data.append({
                        'Timestamp': datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S'),#datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': emotion
                    })
                   
                    global current_activity
                    
                    Emotions_Activities.objects.create(
                        usuario=self.user,
                        activity=current_activity.lower(), #self.data['current_activity'],
                        emotion=emotion,
                        APT1=self.data['APT1'],
                        APT2=self.data['APT2']
                    )

     
            print("%s ends" % (self.getName(),))
        except Exception as e:
            print('Exception in cap creation:',str(e))
            return JsonResponse({'status': 'error', 'message': str(e)})

    def join(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        self.cap.release()
        cv2.destroyAllWindows()
        df = pd.DataFrame(emotion_data)
        df.to_excel('./emotion_data.xlsx', index=False)




class StartEmotionRecognition(View):
    def post(self, request):
        try:
            global th
            cap = cv2.VideoCapture(0)
            respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
            user=request.user
            data = json.load(self.request)
            data['APT1']=respuesta.APT1.lower()
            data['APT2']=respuesta.APT2.lower()
            th=EmotionsThread(cap,user,data)
            th.start()
            return JsonResponse({'status': 'success', 'message': 'Reconocimiento iniciado.'})
        except Exception as e:
            print('Exception in cap creation:',str(e))
            return JsonResponse({'status': 'error', 'message': str(e)})

def close_cap():
    print('cap is going to be released!!')
    try:
        global th
        th.join()
    except NameError as e:
        # Handle the NameError exception
        print(f"NameError occurred: {e}")

# Vista genérica para iniciar sesión
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    def get_success_url(self):        
        close_cap()
        return reverse('home')

# Vista genérica para cerrar sesión
class CustomLogoutView(LogoutView):
    def get_success_url(self):
        # Redirigir al usuario a la vista de fin de actividad después de cerrar sesión
        close_cap()
        return reverse('fin_actividad')
@login_required
def fin_actividad(request):
    close_cap()     
    return render(request, 'fin_actividad.html')


# Vistas para el blog
class InitView(ListView):    
    model = Post
    template_name = 'home.html'
 
#Registro de usuario
def registro_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Vistas adicionales requeridas
@login_required
def test1(request):
    return render(request, 'test1.html')

@login_required
def testuno(request):
    return render(request, 'testuno.html')

@login_required
def test2(request):
    return render(request, 'test2.html')

@login_required
def guardar_respuestas(request):
    if request.method == 'POST':
        
        # Recoge las respuestas del formulario
        
        p1 = int(request.POST.get('p1'))
        p2 = int(request.POST.get('p2'))
        p3 = int(request.POST.get('p3'))
        p4 = int(request.POST.get('p4'))
        p5 = int(request.POST.get('p5'))
        p6 = int(request.POST.get('p6'))
        p7 = int(request.POST.get('p7'))
        p8 = int(request.POST.get('p8'))
        p9 = int(request.POST.get('p9'))
        p10 = int(request.POST.get('p10'))
        p11 = int(request.POST.get('p11'))
        p12 = int(request.POST.get('p12'))
        p13 = int(request.POST.get('p13'))
        p14 = int(request.POST.get('p14'))
        p15 = int(request.POST.get('p15'))
        p16 = int(request.POST.get('p16'))
        p17 = int(request.POST.get('p17'))
        p18 = int(request.POST.get('p18'))
        p19 = int(request.POST.get('p19'))
        p20 = int(request.POST.get('p20'))
        p21 = int(request.POST.get('p21'))
        p22 = int(request.POST.get('p22'))
        p23 = int(request.POST.get('p23'))
        p24 = int(request.POST.get('p24'))
        p25 = int(request.POST.get('p25'))
        p26 = int(request.POST.get('p26'))
        p27 = int(request.POST.get('p27'))
        p28 = int(request.POST.get('p28'))
        p29 = int(request.POST.get('p29'))
        p30 = int(request.POST.get('p30'))
        p31 = int(request.POST.get('p31'))
        p32 = int(request.POST.get('p32'))
        p33 = int(request.POST.get('p33'))
        p34 = int(request.POST.get('p34'))
        p35 = int(request.POST.get('p35'))
        p36 = int(request.POST.get('p36'))
        p37 = int(request.POST.get('p37'))
        p38 = int(request.POST.get('p38'))
        p39 = int(request.POST.get('p39'))
        p40 = int(request.POST.get('p40'))
        p41 = int(request.POST.get('p41'))
        p42 = int(request.POST.get('p42'))
        p43 = int(request.POST.get('p43'))
        p44 = int(request.POST.get('p44'))
        p45 = int(request.POST.get('p45'))
        p46 = int(request.POST.get('p46'))
        p47 = int(request.POST.get('p47'))
        p48 = int(request.POST.get('p48'))
        p49 = int(request.POST.get('p49'))
        p50 = int(request.POST.get('p50'))
        p51 = int(request.POST.get('p51'))
        p52 = int(request.POST.get('p52'))
        p53 = int(request.POST.get('p53'))
        p54 = int(request.POST.get('p54'))
        p55 = int(request.POST.get('p55'))
        p56 = int(request.POST.get('p56'))
        p57 = int(request.POST.get('p57'))
        p58 = int(request.POST.get('p58'))
        p59 = int(request.POST.get('p59'))
        p60 = int(request.POST.get('p60'))
        p61 = int(request.POST.get('p61'))
        p62 = int(request.POST.get('p62'))
        p63 = int(request.POST.get('p63'))
        p64 = int(request.POST.get('p64'))
        p65 = int(request.POST.get('p65'))
        p66 = int(request.POST.get('p66'))
        p67 = int(request.POST.get('p67'))
        p68 = int(request.POST.get('p68'))
        p69 = int(request.POST.get('p69'))
        p70 = int(request.POST.get('p70'))
        p71 = int(request.POST.get('p71'))
        p72 = int(request.POST.get('p72'))
        p73 = int(request.POST.get('p73'))
        p74 = int(request.POST.get('p74'))
        p75 = int(request.POST.get('p75'))
        p76 = int(request.POST.get('p76'))
        p77 = int(request.POST.get('p77'))
        p78 = int(request.POST.get('p78'))
        p79 = int(request.POST.get('p79'))
        p80 = int(request.POST.get('p80'))

        print("respuestas recibidas honey", p1, p2, p3) #prueba

        # Calcula el resultado de cada aprendizaje 
        activo = p3+p5+p7+p9+p13+p20+p26+p27+p35+p37+p27+p41+p43+p46+p48+p51+p61+p67+p74+p75+p77
        reflexivo = p10+p16+p18+p19+p28+p31+p32+p34+p36+p39+p42+p44+p49+p55+p58+p63+p65+p69+p70+p79
        teorico =p2+p4+p6+p11+p15+p17+p21+p23+p25+p29+p33+p45+p50+p54+p60+p64+p66+p71+p78+p80
        pragmatico =p1+p8+p12+p14+p22+p24+p30+p38+p40+p47+p52+p53+p56+p57+p59+p62+p68+p72+p73+p76
       
        cambio=1
        APT1=""

        max_valor1 = max(activo,reflexivo, teorico, pragmatico)

        print("el maximo valor fue: " , max_valor1)
        if max_valor1 == activo:
            print("El estilo predominante en el test 1 es Activo")
            max_valor1="activo"
        elif max_valor1 == reflexivo:
            print("El estilo  predominante en el test 1 es Reflexico")
            max_valor1="reflexivo"
           
        elif max_valor1 == teorico:
            print("El estilo  predominante en el test 1 es Lector Teórico")
            max_valor1="teorico"
            
        else:
            print("El estilo  predominante en el test 1 es Pragmático")
            max_valor1="pragmatico"

        request.session['APT1'] = max_valor1
        request.session['activo'] = activo
        request.session['reflexivo'] = reflexivo
        request.session['teorico'] = teorico
        request.session['pragmatico'] = pragmatico

        print(f"APT1 guardado en la sesión: {request.session['APT1']}")

        resultado1 = {
            'activo': activo,
            'reflexivo': reflexivo,
            'teorico': teorico,
            'pragmatico': pragmatico,
            'siguienteTest':cambio,
            'APT1':max_valor1, 
        }  

        print("Resultados procesados Test 1: ", resultado1)  # Verifica si se están calculando correctamente
        return render(request, 'resultadostest.html', resultado1)
        return redirect(reverse('testdos.html'))  # Redirige a la siguiente página del test
        
    return HttpResponse("Método no permitido", status=405)

@login_required
def guardar_respuestast2(request):
    if request.method == 'POST':
        # Inicializar los contadores para cada estilo de aprendizaje
        
        visual = 0
        auditivo = 0
        lector_escrito = 0
        kinestesico = 0
        cambio = 2
        
        # Variables del test anterior CHAE
        activo = request.session.get('activo', '')
        reflexivo = request.session.get('reflexivo', '')
        teorico = request.session.get('teorico', '')
        pragmatico = request.session.get('pragmatico', '')
        APT1 = request.session.get('APT1', '')
        
        # Recoger las respuestas del formulario
        respuestas = {
            'p1': request.POST.get('p1'),
            'p2': request.POST.get('p2'),
            'p3': request.POST.get('p3'),
            'p4': request.POST.get('p4'),
            'p5': request.POST.get('p5'),
            'p6': request.POST.get('p6'),
            'p7': request.POST.get('p7'),
            'p8': request.POST.get('p8'),
            'p9': request.POST.get('p9'),
            'p10': request.POST.get('p10'),
            'p11': request.POST.get('p11'),
            'p12': request.POST.get('p12'),
            'p13': request.POST.get('p13'),
            'p14': request.POST.get('p14'),
            'p15': request.POST.get('p15'),
            'p16': request.POST.get('p16'),
        }

        print("Respuestas recibidas: ", respuestas)  # Imprimir para verificar

        # Sumar las respuestas a cada estilo de aprendizaje
        for respuesta in respuestas.values():
            if respuesta == 'v':  # visual
                visual += 1
            elif respuesta == 'a':  # auditivo
                auditivo += 1
            elif respuesta == 'r':  # lector/escrito
                lector_escrito += 1
            elif respuesta == 'k':  # kinestésico
                kinestesico += 1


        # Encontrar el estilo con el valor más alto
        max_valor2 = max(visual, auditivo, lector_escrito, kinestesico)
        
        print("el maximo valor fue: " , max_valor2)
        if max_valor2 == visual:
            print("El estilo predominante en el test 2 es Visual")
            APT2 = "Visual"
        elif max_valor2 == auditivo:
            print("El estilo  predominante en el test 2 es Auditivo")
            APT2 = "Auditivo"
        elif max_valor2 == lector_escrito:
            print("El estilo  predominante en el test 2 es Lector Escrito")
            APT2 = "Escrito"
        else:
            print("El estilo  predominante en el test 2 es kinestésico")
            APT2 = "Kinestésico"


          
        # Guardar APT2 en la sesión y en la base de datos
        request.session['APT2'] = APT2
        EA_Respuestas.objects.update_or_create(
            usuario=request.user,
            defaults={'APT1': APT1, 'APT2': APT2}
        )
        
        
        # Redirigir o renderizar la página de resultados
        return render(request, 'resultadostest.html', {
            'visual': visual,
            'auditivo': auditivo,
            'lector_escrito': lector_escrito,
            'kinestesico': kinestesico,
            'siguienteTest': cambio,
            'APT2': APT2,
            'APT1': APT1,
            'activo': activo,
            'reflexivo': reflexivo,
            'teorico': teorico,
            'pragmatico': pragmatico,
        })

    return HttpResponse("Método no permitido", status=405)

    
@login_required
def resultadostest(request):
     # Obtén los resultados del usuario actual
    respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
    if not respuesta:
        context = {
            'Test_CHAE': None,
            'Test_VARK': None
        }
        
    else:
        context = {
            'Test_CHAE': respuesta.APT1,
            'Test_VARK': respuesta.APT2,
        }
        
    return render(request, 'resultadostest.html', context)

@login_required
def testdos(request):
    return render(request, 'testdos.html')
    
@login_required
def actividad1(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_url = fs.url(filename)
        return render(request, 'actividad1.html', {'file_url': file_url})
    return render(request, 'actividad1.html')

@login_required
def actividad2(request):
    return render(request, 'actividad2.html')

@login_required
def actividad3(request):
    return render(request, 'actividad3.html')

@login_required
def actividadActivo(request):
    respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
    
    if not respuesta:
        context = {
            'Test_CHAE': None,
            'Test_VARK': None
        }
        print("este es ", context)
    else:
        context = {
            'Test_CHAE': respuesta.APT1,
            'Test_VARK': respuesta.APT2,
        }
        print("este es :) ", context)
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Activo"
                    })
    global current_activity
    current_activity='Activo'
    return render(request, 'actividadActivo.html', context)


@login_required
def actividadTeorica(request):
    respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
    
    if not respuesta:
        context = {
            'Test_CHAE': None,
            'Test_VARK': None
        }
        print("este es ", context)
    else:
        context = {
            'Test_CHAE': respuesta.APT1,
            'Test_VARK': respuesta.APT2
        }
        print("este es :) ", context)

    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Teórica"
                    })
    global current_activity
    current_activity='Teórico'
    return render(request, 'actividadTeorica.html', context)


@login_required
def actividadPragmatica(request):
    respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
    
    if not respuesta:
        context = {
            'Test_CHAE': None,
            'Test_VARK': None
        }
        print("este es ", context)
    else:
        context = {
            'Test_CHAE': respuesta.APT1,
            'Test_VARK': respuesta.APT2
        }
        print("este es :) ", context)
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Pragmática"
                    })
    global current_activity
    current_activity='Pragmático'
    return render(request, 'actividadPragmatica.html', context)    

@login_required
def actividadReflexiva(request):
    respuesta = EA_Respuestas.objects.filter(usuario=request.user).first()
    
    if not respuesta:
        context = {
            'Test_CHAE': None,
            'Test_VARK': None
        }
        print("este es ", context)
    else:
        context = {
            'Test_CHAE': respuesta.APT1,
            'Test_VARK': respuesta.APT2
        }
        print("este es :) ", context)
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Reflexiva"
                    })
    global current_activity
    current_activity='Reflexivo'
    return render(request, 'actividadReflexiva.html', context)    

@login_required
def actividadVisual(request):
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Visual"
                    }) 
    global current_activity
    current_activity='Visual'
    return render(request, 'actividadVisual.html')

@login_required
def actividadKinestesico(request):
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Kinestésico"
                    })
    global current_activity
    current_activity='Kinestésico'
    return render(request, 'actividadKinestesico.html')

@login_required
def actividadAuditivo(request):
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Auditiva"
                    })
    global current_activity
    current_activity='Auditivo'
    return render(request, 'actividadAuditivo.html')

@login_required
def actividadLE(request):
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_LE"
                    })
    global current_activity
    current_activity='LE'
    return render(request, 'actividadLE.html')

@login_required
def actividadAleatoria(request):
    emotion_data.append({
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'Emotion': "Actividad_Aleatoria"
                    })
    global current_activity
    current_activity='Aleatorio'
    return render(request, 'actividadAleatoria.html')

@login_required
def charts(request):
    emotions = ['Feliz','Neutral','Enojado','Asustado','Triste','Sorprendido']
    
    profilesCHAEA = ['Activo','Reflexivo','Teórico','Pragmático']
    profilesCHAEACount = []
    
    profilesVARK = ['visual','Auditivo','Lecto-Escritor','Kinestésico']
    profilesVARKCount = []
    
    happyQ = Emotions_Activities.objects.filter(emotion='happy')
    neutralQ = Emotions_Activities.objects.filter(emotion='neutral')
    angryQ = Emotions_Activities.objects.filter(emotion='angry')
    fearQ = Emotions_Activities.objects.filter(emotion='fear')
    sadQ = Emotions_Activities.objects.filter(emotion='sad')
    surpQ = Emotions_Activities.objects.filter(emotion='surprise')
    
   
    activos = Emotions_Activities.objects.filter(activity='activo',APT1='activo')
    profilesCHAEACount.append(activos.count())
    reflexivos = Emotions_Activities.objects.filter(activity='reflexivo',APT1='reflexivo')
    profilesCHAEACount.append(reflexivos.count())
    teoricos = Emotions_Activities.objects.filter(activity='teórico',APT1='teorico')
    profilesCHAEACount.append(teoricos.count())
    pragmaticos = Emotions_Activities.objects.filter(activity='pragmático',APT1='pragmatico')
    profilesCHAEACount.append(pragmaticos.count())
    
    visuales = Emotions_Activities.objects.filter(activity='visual',APT2='visual')
    profilesVARKCount.append(visuales.count())
    auditivos = Emotions_Activities.objects.filter(activity='auditivo',APT2='auditivo')
    profilesVARKCount.append(auditivos.count())
    LEs = Emotions_Activities.objects.filter(activity='le',APT2='escrito')
    profilesVARKCount.append(LEs.count())
    kinestesicos = Emotions_Activities.objects.filter(activity='kinestésico',APT2='kinestésico')
    profilesVARKCount.append(kinestesicos.count())
    
    
    
    listsCHAEA=[[a.emotion for a in activos], [r.emotion for r in reflexivos], [t.emotion for t in teoricos], [p.emotion for p in pragmaticos]]
    
    emotionsCountCH=[sum(lst.count("happy") for lst in listsCHAEA),
                     sum(lst.count("neutral") for lst in listsCHAEA), 
                     sum(lst.count("angry") for lst in listsCHAEA), 
                     sum(lst.count("fear") for lst in listsCHAEA), 
                     sum(lst.count("sad") for lst in listsCHAEA), 
                     sum(lst.count("surprise") for lst in listsCHAEA)]
    
    listsVARK=[[v.emotion for v in visuales], [a.emotion for a in auditivos], [LE.emotion for LE in LEs], [k.emotion for k in kinestesicos]]
    
    emotionsCountVARK=[sum(lst.count("happy") for lst in listsVARK),
                       sum(lst.count("neutral") for lst in listsVARK),
                       sum(lst.count("angry") for lst in listsVARK),
                       sum(lst.count("fear") for lst in listsVARK),
                       sum(lst.count("sad") for lst in listsVARK),
                       sum(lst.count("surprise") for lst in listsVARK)
    ]
    
    aleatorio = Emotions_Activities.objects.filter(activity='aleatorio')
    listsRand=[a.emotion for a in aleatorio]
    emotionsCountRand=[sum(lst.count("happy") for lst in listsRand),
                       sum(lst.count("neutral") for lst in listsRand),
                       sum(lst.count("angry") for lst in listsRand),
                       sum(lst.count("fear") for lst in listsRand),
                       sum(lst.count("sad") for lst in listsRand),
                       sum(lst.count("surprise") for lst in listsRand)
    ]
    
    
    print('Emotions CHAEA:',emotionsCountCH)
    print('Emotions VARK:',emotionsCountVARK)
    return render(request, 'charts.html', {
        'emotions': emotions,
        'emotionsCountCH': emotionsCountCH,
        'emotionsCountVARK': emotionsCountVARK,
        'emotionsCountRand': emotionsCountRand,
        'profilesCHAEA': profilesCHAEA,
        'profilesCHAEACount': profilesCHAEACount,
        'profilesVARK' : profilesVARK,
        'profilesVARKCount' : profilesVARKCount
    })

