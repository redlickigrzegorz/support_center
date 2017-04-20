from django.template import loader
from django.http import HttpResponse
from .models import Fault, Object
from django.http import Http404
from .forms import AdminFaultForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


@login_required
@staff_member_required
def index(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status__in=[0, 1])

    context = {'faults': faults,
               'header': 'all faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def my_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, handler=request.user.username)

    context = {'faults': faults,
               'header': 'faults assigned to me'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def resolved_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=True, status=2)

    context = {'faults': faults,
               'header': 'resolved faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def deleted_faults(request):
    template = loader.get_template('cti/admin/index.html')

    faults = Fault.objects.filter(is_visible=False)

    context = {'faults': faults,
               'header': 'deleted faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def edit_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        template = loader.get_template('cti/admin/fault_form.html')

        form = AdminFaultForm(request.POST or None, instance=fault)

        if request.method == "POST":
            if form.is_valid():
                fault = form.save(commit=False)
                fault.save()
                messages.success(request, "fault edited successful")
            else:
                for field in form:
                    for error in field.errors:
                        messages.warning(request, "{} - {}".format(field.name, error))

        context = {'form': form,
                   'button': 'edit',
                   'header': 'edit fault'}

        return HttpResponse(template.render(context, request))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def delete_fault(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.is_visible:
            fault.is_visible = False
            fault.save()
            messages.success(request, "fault deleted successful")
        else:
            messages.warning(request, "fault is already deleted")

        return HttpResponseRedirect(reverse('cti:index_admin'))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def assign_to_me(request, fault_id):
    try:
        fault = Fault.objects.get(pk=fault_id)

        if fault.handler == '0':
            fault.handler = request.user.get_username()
            fault.status = 1
            fault.save()
            messages.success(request, "fault assigned successful")
        else:
            messages.warning(request, "fault is already assigned")

        return HttpResponseRedirect(reverse('cti:index_admin'))

    except Fault.DoesNotExist:
        raise Http404("fault does not exist")


@login_required
@staff_member_required
def fault_details(request, fault_id):
    template = loader.get_template('cti/admin/fault_details.html')

    try:
        fault = Fault.objects.get(pk=fault_id)
        context = {'fault': fault,
                   'header': 'fault\'s details'}
    except Fault.DoesNotExist:
        raise Http404("fault does not exist")

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def object_details(request, object_id):
    template = loader.get_template('cti/admin/object_details.html')

    try:
        object = Object.objects.get(object_number=object_id)
        context = {'object': object,
                   'header': 'object\'s details'}
    except Object.DoesNotExist:
        raise Http404("object does not exist")

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def user_details(request):
    template = loader.get_template('cti/admin/user_details.html')

    User = get_user_model()

    try:
        user = User.objects.get(username__exact=request.user)
        context = {'user': user,
                   'header': 'user\'s details'}
    except User.DoesNotExist:
        raise Http404("user does not exist")

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def all_users(request):
    template = loader.get_template('cti/admin/users.html')

    User = get_user_model()

    users = User.objects.all()

    context = {'users': users,
               'header': 'all faults'}

    return HttpResponse(template.render(context, request))


@login_required
@staff_member_required
def change_password(request):
    template = loader.get_template('cti/change_password.html')

    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        new_password_repeat = request.POST['new_password_repeat']

        user = User.objects.get(username__exact=request.user)

        if new_password != new_password_repeat:
            messages.warning(request, 'new password fields are different! ')

        if not user.check_password(old_password):
            messages.warning(request, 'old password is wrong')

        if user.check_password(old_password) and new_password == new_password_repeat:
            user.set_password(new_password)
            user.save()
            user = authenticate(username=request.user, password=new_password)
            auth.login(request, user)
            messages.success(request, 'password has been changed')

            return HttpResponseRedirect(reverse('cti:index'))

    return HttpResponse(template.render(request))