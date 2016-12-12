from django.template import loader
from django.http import HttpResponse
from .models import Fault
from django.http import Http404
from .forms import FaultForm


def index(request):
    template = loader.get_template('cti/index.html')
    faults = Fault.objects.all()

    context = {'faults': faults,
               'fields': Fault().get_fields(), }

    return HttpResponse(template.render(context, request))


def detail(request, fault_id):
    template = loader.get_template('cti/detail.html')
    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault }
    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")

    return HttpResponse(template.render(context, request))


def add_fault(request):
    template = loader.get_template('cti/add_fault.html')

    if request.method == "POST":
        form = FaultForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.save()
    else:
        form = FaultForm()

    context = {'form': form}

    return HttpResponse(template.render(context, request))

def edit_fault(request, fault_id):
    template = loader.get_template('cti/edit_fault.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        form = FaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()

        context = {'form': form}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("Fault does not exist")