from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

#import the model associated w/the data we need
from .models import Topic, Entry 
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
	"""The home page for Learning Log."""
	return render(request, 'learning_logs/index.html')

@login_required
def new_topic(request):
	"""Add new topic"""
	if request.method != 'POST':
		# No data submnitted; create a blank form.
		form = TopicForm()
	else:
		#$ POST data submitted; process data.
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect('learning_logs:topics')

	# Display a blank or invalid form.
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)

@login_required #awesome decorator that adds privacy to topics
def topics(request):
	"""Show all topics."""
	#query the db asking for topic objects
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')

	#define the context we'll send to the template
	context = {'topics': topics}
	#define where to send the data; pass context variable to render(), along w/request object, 
	# and the path to template
	return render(request, 'learning_logs/topics.html', context)

# the topic() function needs to get the topic, all associated entries from the db:
@login_required
def topic(request, topic_id):
	"""Show a single topic and all its entries"""
	topic = Topic.objects.get(id=topic_id)	#query db
	entries = topic.entry_set.order_by('-date_added')	#query db
	context = {'topic': topic, 'entries': entries}	#key-value dictionary
	return render(request, 'learning_logs/topic.html', context)

@login_required
def new_entry(request, topic_id):
	"""Add a new entry for a particular topic."""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		# POST data submitted; process data. 
		form = EntryForm()
	else:
		# Post data submitted; process data.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)
		
	# Display a blank or invalid form. 
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	""" Edit an existing entry"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic 

	if request.method != 'POST':
		# Initial request; pre-fill form with the current entry
		form = EntryForm(instance=entry)
	else:
		# POST data submitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)

	context = {'entry': entry, 'topic':topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)

