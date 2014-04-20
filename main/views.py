from django.shortcuts import render
from main.models import Ship, Container, Dock, Employee, DockHistory
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from main.util import get_unique_id, get_available_elements, get_connected_elements

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
        context['available_ships'] = get_available_elements(Ship, 'dock', Dock)
        context['available_docks'] = get_available_elements(Dock, 'ship')
        context['available_employees'] = get_available_elements(Employee, 'assigned_to')
        return context

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
            dock_id = request.POST.get('occupy_dock', '')
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

        elif action=="placeemployee":
            # Places a ship in a given dock
            dock_id = request.POST.get('assign_to_dock', '')
            employee_id = request.POST.get('employee_id', '')
            dock = Dock.objects.get(pk=int(dock_id))
            employee = Employee.objects.get(id=employee_id)

            employee.assigned_to = dock
            employee.save()

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
        context['available_containers'] = get_available_elements(Container, 'ship')
        context['assigned_employees'] = get_connected_elements(Employee, 'assigned_to',
                                                               self.get_object())
        context['dock_history'] = DockHistory.objects.filter(dock=self.get_object()).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        current_dock_pk = int(kwargs['pk'])
        current_dock = Dock.objects.get(pk=current_dock_pk)
        action = request.POST.get('action')

        if action == 'createcontainer':
            container_uid = get_unique_id(6, Container, 'uid')
            is_flamable = bool(request.POST.get('flamable', ''))
            is_chemical_hazard = bool(request.POST.get('chemicalhazard', ''))

            container = Container.objects.create(
                uid=container_uid, is_flamable=is_flamable,
                is_chemical_hazard=is_chemical_hazard, ship=None)

        elif action == 'containercontrol':
            move_containers = request.POST.getlist('move_containers')
            place_container = bool(request.POST.get("placecontainer"))
            delete_container = bool(request.POST.get("deletecontainer"))
            print place_container, delete_container

            if move_containers:
                if place_container:
                    ship = Ship.objects.get(uid=request.POST.get('ship_id', ''))

                    for move_uid in move_containers:
                        container = Container.objects.get(uid=move_uid)
                        container.ship = ship
                        container.save()

                elif delete_container:
                    for move_uid in move_containers:
                        container = Container.objects.get(uid=move_uid)
                        container.delete()

        elif action == 'removecontainer':
            container = Container.objects.get(uid=request.POST['container_uid'])
            container.ship = None
            container.save()

        elif action == 'releaseemployee':
            employee = Employee.objects.get(id=request.POST['employee_id'])
            employee.assigned_to = None
            employee.save()

        return HttpResponseRedirect(reverse(('dock_detail'), kwargs={'pk': current_dock_pk}))
