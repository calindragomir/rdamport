from django.shortcuts import render
from main.models import Ship, Container, Dock, Employee, DockHistory
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from main.util import get_unique_id

import datetime

# Create your views here.
class PortView(TemplateView):
    """
    Returns an overview of the port
    """

    template_name = 'overview.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PortView, self).get_context_data(**kwargs)
        # Add the information we need in context
        context['docks'] = Dock.objects.all()
        context['available_ships'] = self.get_available_ships()
        context['available_docks'] = self.get_available_docks()
        return context

    def get_available_docks(self):
        dock_instances = Dock.objects.all()
        available_docks = []

        for dock in dock_instances:
            if not dock.ship:
                available_docks.append(dock)

        return available_docks

    def get_available_ships(self):
        ship_instances = Ship.objects.all()
        available_ships = []

        for ship in ship_instances:
            try:
                dock = ship.dock
            except Dock.DoesNotExist:
                available_ships.append(ship)

        return available_ships

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        # Identify which action needs to be performed
        if action == 'cleardock':
            # Clears current dock
            dock_id = request.POST['cleared_dock']
            ship_id = request.POST['removed_ship']
            dock = Dock.objects.get(id=dock_id)
            ship = Ship.objects.get(uid=ship_id)
            dock_history = DockHistory.objects.filter(dock=dock, ship=ship)

            # Remove ship from dock
            dock.ship = None
            dock.save()

            # Find the current ship log item and store departure time
            for history_item in dock_history:
                if not history_item.date_out:
                    history_item.date_out = datetime.datetime.now()
                    history_item.save()
                    break

        elif action=="adddock":
            # Adds a new dock to the database
            dock_name = request.POST.get('dockname', '')

            if not dock_name:
                return HttpResponseRedirect(reverse('port'))

            dock, created = Dock.objects.get_or_create(name=dock_name)

        elif action=="placeship":
            # Places a ship in a given dock
            dock_id = request.POST.get('free_dock', '')
            ship_uid = request.POST.get('ship_id', '')
            dock = Dock.objects.get(pk=int(dock_id))
            ship = Ship.objects.get(uid=ship_uid)

            try:
                dock.ship = ship
                dock.save()
            except IntegrityError:
                pass

            # Record entry of ship in dock log
            dock_history = DockHistory.objects.create(
                            dock=dock,
                            ship=ship,
                            date_in=datetime.datetime.now())

        elif action=="generateship":
            # Generates a new ship record
            uid = get_unique_id(6, Ship, 'uid')
            ship, created = Ship.objects.get_or_create(uid=uid)

        elif action=="removeship":
            # Deletes a ship record
            ship_uid = request.POST.get('ship_id', '')
            ship = Ship.objects.get(uid=ship_uid)
            ship.delete()

        return HttpResponseRedirect(reverse('port'))

class DockDetailView(DetailView):
    """
    Returns all details about a given dock
    """
    template_name = 'detail.html'
    model = Dock

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DockDetailView, self).get_context_data(**kwargs)
        # Add the information we need in context
        return context
