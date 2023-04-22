from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import InsuranceForm
from django.contrib import messages
from .models import Insurance
import re

def insurance_dashboard(request):
    user = request.user.email
    # email = ""
    # if re.search(".@gmail.com$", user):
    #     email = "yes" 
    #     return redirect('patient_dashboard')
    submitted = False
    if request.method == "POST":
        form = InsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/insurance_provider/dashboard?submitted=True')
    else:
        form = InsuranceForm
        if 'submitted' in request.GET:
            submitted = True
            messages.success(request, ("New Insurance added Successfully"))

    insurance_list = Insurance.objects.all()

    count = 0
    for insurance in insurance_list:
        count = count+1
        insurance.display_id = count
    return render(request, 'insurance_dashboard.html', {'form': form, 'submitted': submitted, 'insurance_list': insurance_list})

def insurance_detail(request, insurance_id):
    insurance = Insurance.objects.get(pk=insurance_id)
    return render(request, 'insurance_detail.html', {'insurance': insurance})

def delete_insurance(request, insurance_id):
    insurance = Insurance.objects.get(pk=insurance_id)
    insurance.delete()
    messages.info(request, ("Insurance Deleted"))
    return redirect('insurance_dashboard')

