from django.shortcuts import render, redirect
from .models import Person,Identy,Jharsewa,Education
# Create your views here.
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
class PersonListView(generic.ListView):
    model = Person
from django.contrib.auth.mixins import LoginRequiredMixin
class PersonDetailView(LoginRequiredMixin,generic.DetailView):
    model = Person
    def get_queryset(self):
        return Person.objects.filter(django_username=self.request.user)
#from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
# Import User UpdateForm, ProfileUpdatForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,IdentyUpdateForm, JharsewaForm, EducationForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_person = Person.objects.all().count()
    num_id = Identy.objects.all().count()

    # Available books (status = 'a')
    #num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #num_instances_borrowed=BookInstance.objects.filter(borrower=request.user.borro>
    # The 'all()' is implied by default.
    num_jhar = Jharsewa.objects.count()

    num_edu=Education.objects.count()
    #session
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_person': num_person,
        'num_id': num_id,
        #'num_instances_available': num_instances_available,
        #'num_instances_borrowed': num_instances_borrowed,
        'num_jhar': num_jhar,
        'num_edu':num_edu,
        'num_visits': num_visits,

    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'person/index.html', context=context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) 
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username') 
            messages.success(request, f'Your account has been created! You are now able to log in') 
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'person/register.html', {'form': form})

# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.person) 
        if u_form.is_valid() and p_form.is_valid():
            id=p_form.save(commit=False)
            id.django_username = request.user
            id.save()
            u_form.save()
            #id.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/home') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.person)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'person/profile.html', context)

@login_required
def identy(request):
    i_form = IdentyUpdateForm({"person":request.user})
    if request.method == 'POST':
        #u_form = UserUpdateForm(request.POST, instance=request.user)
        #p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.person)
        i_form = IdentyUpdateForm(request.POST,request.FILES)
        if i_form.is_valid():
            id=i_form.save(commit=False)
            id.person = request.user.person
            id.save()
            messages.success(request, f'Your account id  has been updated!')
            return redirect('/home') # Redirect back to profile page

    else:
        #u_form = UserUpdateForm(instance=request.user)
        #p_form = ProfileUpdateForm(instance=request.user.person)
        i_form = IdentyUpdateForm()
    context = {
        'i_form': i_form,
    }

    return render(request, 'person/identy.html', context)

def jharsewa(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JharsewaForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            jhar=form.save(commit=False)
            jhar.person = request.user.person
            jhar.save()
            # process the data in form.cleaned_data as required
            #form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JharsewaForm()
    return render(request, 'person/jharsewa.html', {'form': form})



def edu(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EducationForm(request.POST,request.FILES)
        # check whether it's valid:
        if form.is_valid():
            edud=form.save(commit=False)
            edu.person = request.user.person
            edu.save()
            #form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EducationForm()
    return render(request, 'person/edu.html', {'form': form})

from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
@login_required
def idupdate(request,pk):
    idinst=Identy.objects.get(pk=pk)
    i_form = IdentyUpdateForm(initial=model_to_dict(idinst))
    if request.method == 'POST':
        i_form = IdentyUpdateForm(request.POST,request.FILES,instance=idinst)
        if i_form.is_valid():
            edu=i_form.save(commit=False)
            edu.person = request.user.person
            edu.save()
            return HttpResponseRedirect('/home')
    context = {
        'i_form': i_form,
    }

    return render(request, 'person/identy.html', context)

@login_required
def jharupdate(request,pk):
    idinst=Jharsewa.objects.get(pk=pk)
    i_form = JharsewaForm(initial=model_to_dict(idinst))
    if request.method == 'POST':
        i_form = JharsewaForm(request.POST,request.FILES,instance=idinst)
        if i_form.is_valid():
            edu=i_form.save(commit=False)
            edu.person = request.user.person
            edu.save()
            return HttpResponseRedirect('/home')
    context = {
        'i_form': i_form,
    }

    return render(request, 'person/identy.html', context)


@login_required
def eduupdate(request,pk):
    idinst=Education.objects.get(pk=pk)
    i_form = EducationForm(initial=model_to_dict(idinst))
    if request.method == 'POST':
        i_form = EducationForm(request.POST,request.FILES,instance=idinst)
        if i_form.is_valid():
            edu=i_form.save(commit=False)
            edu.person = request.user.person
            edu.save()
            return HttpResponseRedirect('/home')
    context = {
        'i_form': i_form,
    }

    return render(request, 'person/identy.html', context)



@login_required
def id_del(request,pk):
    context ={}
    idinst=get_object_or_404(Identy,pk=pk)
    if request.method == 'POST':
        #u_form = UserUpdateForm(request.POST, instance=request.user)
        #p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.us>
        #i_form = IdentyUpdateForm(request.POST,request.FILES,instance=idinst)
        #if i_form.is_valid():
        idinst.delete()
        messages.success(request, f'Your one id  has been deleted!')
        return redirect('/home') # Redirect back to profile page

    return render(request, 'person/id_del.html', context)

def home(request):
    person=Person.objects.get(django_username=request.user)
    context={"person":person,}
    return render(request, 'person/detail.html', context=context)

@login_required
def jhar_del(request,pk):
    context ={}
    jharid=get_object_or_404(Jharsewa,pk=pk)
    if request.method == 'POST':
        #u_form = UserUpdateForm(request.POST, instance=request.user)                           #p_form = ProfileUpdateForm(request.POST, request.FILES,instance=requ          >        #i_form = IdentyUpdateForm(request.POST,request.FILES,instance=idinst)
        #if i_form.is_valid():
        jharid.delete()
        messages.success(request, f'Your one id  has been deleted!')
        return redirect('/home') # Redirect back to profile page

    return render(request, 'person/id_del.html', context)


@login_required
def edu_del(request,pk):
    context ={}
    jharid=get_object_or_404(Education,pk=pk)
    if request.method == 'POST':
        #u_form = UserUpdateForm(request.POST, instance=request.user)>
        #if i_form.is_valid():
        jharid.delete()
        messages.success(request, f'Your one edu id  has been deleted!')
        return redirect('/home') # Redirect back to profile page

    return render(request, 'person/id_del.html', context)

import subprocess
#pdf
@login_required
def pdf(request, pk):

    #Get the applicant's resume
    pdff = Identy.objects.get(pk=pk)
    #with subprocess.Popen([pdff.idcard],) as pdf:
    #response = HttpResponse(pdff.idcard)
    response = HttpResponse(pdff.idcard.read(),content_type='application/pdf' )
    response['Content-Disposition'] = 'inline;'
        #response = HttpResponse(fsock, mimetype='application/pdf')

    return response

    #pdf.closed
