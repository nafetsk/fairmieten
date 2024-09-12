from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Hello
from .forms import HelloForm

# REST Views.

def hello(request):
	name = request.GET.get('name')
	greetings = Hello.objects.all();
	return render(request, "hello.html", {"name":name, "greetings":greetings})


def hello_new(request):
	if request.method == "POST":
		form = HelloForm(request.POST)
		if form.is_valid():
				post = form.save(commit=False)
				post.published_date = timezone.now()
				post.save()
				return redirect('hello_list')    
	else:
		form = HelloForm()    
		return render(request, 'hello_add.html', {'form': form})


