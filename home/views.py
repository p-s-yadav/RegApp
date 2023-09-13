from django.shortcuts import render, redirect
from .forms import RegForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import DocumentForm
from .models import Documents
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pandas as pd
from django.conf import settings
from django.core.mail import send_mail

def show(r):
    return render(r, 'home.html')


def RegView(r):
    if r.method == "POST":
        print("post request")
        form = RegForm(r.POST)
        if form.is_valid():
            user = form.save()

            # Send a welcome email to the registered user
            # subject = 'Welcome to WebPage'
            # message = 'Thank you for registering on our website. We hope you enjoy your experience!'
            # from_email = 'testinge536@gmail.com'
            # recipient_list = ['testinge536@gmail.com']

            # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('loginname')
    form = RegForm()
    return render(r, "register.html", context= {"register_form": form} )

        
def login_request(r):
    if r.method == "POST":
        form = AuthenticationForm(r, data=r.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(r, user)
                messages.info(r, f"You are now logged in as {username}.")
                return redirect('upload')
            else:
                messages.error(r,"Invalid username or password.")
        else:
            messages.error(r,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=r, template_name="loginnew.html", context={"login_form":form})


def logout_request(r):
	logout(r)
	messages.info(r, "You have successfully logged out.") 
	return redirect("home")


def upload(r):
	form = DocumentForm()
	if r.method == "POST":
		form = DocumentForm(r.POST, r.FILES)
		if form.is_valid():
			file_instance = form.save(commit=False)
			file_instance.user = r.user
			file_instance.save()
			return redirect('file_list')
		else:
			form = DocumentForm()
		return render(r, 'upload.html', {'form': form})
	return render(r, 'upload.html', {'form': form})


def file_list(r):
    files = Documents.objects.filter(user=r.user).order_by('-update_date')
    return render(r, 'file_list.html', {'files': files})


def download_file(r, file_id):
    uploaded_file = Documents.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response


def delete_file(request, file_id):
    document = get_object_or_404(Documents, pk=file_id)
    if document.user == request.user:
        document.delete_document()
    return redirect('file_list')


def update_file(r, file_id):
    document = get_object_or_404(Documents, pk=file_id)

    if r.method == "POST":
        form = DocumentForm(r.POST, r.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            document.update_document(new_file.file, new_file.description)
            return redirect('file_list')
    else:
        form = DocumentForm(instance=document)
    
    return render(r, 'update_file.html', {'form': form})

def download_list(r):
      file_list = Documents.objects.values()
      df = pd.DataFrame(file_list)
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="list_of_uploads.csv"'
      df.to_csv(path_or_buf=response)
      return response
      