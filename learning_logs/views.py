from django.shortcuts import render

#import the model associated w/the data we need
from .models import Topic 

# Create your views here.
def index(request):
	"""The home page for Learning Log."""
	return render(request, 'learning_logs/index.html')


def topics(request):
	"""Show all topics."""
	#query the db asking for topic objects
	topics = Topic.objects.order_by('date_added')

	#define the context we'll send to the template
	context = {'topics': topics}
	#define where to send the data; pass context variable to render(), along w/request object, 
	# and the path to template
	return render(request, 'learning_logs/topics.html', context)

# the topic() function needs to get the topic, all associated entries from the db:
def topic(request, topic_id):
	"""Show a single topic and all its entries"""
	topic = Topic.objects.get(id=topic_id)	#query db
	entries = topic.entry_set.order_by('-date_added')	#query db
	context = {'topic': topic, 'entries': entries}	#key-value dictionary
	return render(request, 'learning_logs/topic.html', context)