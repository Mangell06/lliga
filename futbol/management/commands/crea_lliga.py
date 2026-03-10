from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import time
from datetime import timedelta, datetime
import random
import math
 
from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga, temporada="temporada" )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[random.randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(ciutat=ciutat,nom=nom,lliga=lliga)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                edat = random.randint(17,38);
                jugador = Jugador(nom=nom,posicio=posicio,
                    edat=edat,equip=equip)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    mes = random.randint(1,11)
                    dia = random.randint(1,27)
                    hora = random.randint(16,20)
                    minut = random.randint(0,59)
                    partit.inici = timezone.make_aware(datetime(2026, int(mes), int(dia), int(hora), int(minut)))
                    partit.save()

                    # Máximo de goles posibles
                    max_goles = 6

                    # Generar pesos decrecientes automáticamente
                    distribucion_goles = list(range(max_goles + 1))
                    pesos = [1 / (1 + g) for g in distribucion_goles]

                    # Elegir número de goles con más probabilidad para los valores bajos
                    num_goles = random.choices(distribucion_goles, pesos)[0]

                    # Generar tiempos únicos y ordenados
                    tiempos = set()
                    while len(tiempos) < num_goles:
                        minut = random.randint(0, 89)
                        segon = random.randint(0, 59)
                        tiempos.add((minut, segon))

                    tiempos = sorted(tiempos)

                    for minut_joc, segon in tiempos:
                        tipus = Event.EventType.GOL
                        equip_gol = local if random.random() < 0.5 else visitant

                        jugador = (
                            Jugador.objects
                            .filter(equip=equip_gol)
                            .order_by("?")
                            .first()
                        )

                        hores_real = minut_joc // 60
                        minuts_real = minut_joc % 60

                        event = Event(
                            partit=partit,
                            temps=time(hores_real, minuts_real, segon), 
                            tipus=tipus,
                            jugador=jugador,
                            equip=equip_gol
                        )
                        event.save()