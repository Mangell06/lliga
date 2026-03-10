from django.contrib import admin
from .models import *
 
admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
class EventInline(admin.TabularInline):
    exclude  = ["detalls"]
    model = Event
    extra = 3
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        partit_id = request.resolver_match.kwargs.get('object_id')
        if partit_id:
            partit = Partit.objects.get(id=partit_id)
            if db_field.name == "jugador":
                partit_id = request.resolver_match.kwargs['object_id']
                partit = Partit.objects.get(id=partit_id)
                jugadors_local = [jugador.id for jugador in partit.local.jugadors.all()]
                jugadors_visitant = [jugador.id for jugador in partit.visitant.jugadors.all()]
                jugadors = jugadors_local + jugadors_visitant
                kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors)
            elif db_field.name == "equip":
                equip_local = partit.local.id
                equip_visitant = partit.visitant.id
                equips = [equip_local, equip_visitant]
                kwargs["queryset"] = Equip.objects.filter(id__in=equips)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PartitAdmin(admin.ModelAdmin):
    search_fields = ["local__nom", "visitant__nom", "lliga__nom"]
    list_display = ["lliga" , "local", "visitant", "gols_local", "gols_visitant"]
    inlines = [EventInline]


admin.site.register(Partit, PartitAdmin)