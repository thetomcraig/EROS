import urllib
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from scrapers.models.plain_text_classes import Sentence, Person, MarkovChain
from scrapers import utils
from datetime import datetime


usage = "python manage intake_plain_text " + \
				"--file_name <name> " + \
				"--author <name> " + \
				"[--sentiment_analyze] " + \
				"[--apply_markov_chains id=id|all] "

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('--file_name', default=False)
		parser.add_argument('--author', default=False)
		parser.add_argument('--sentiment_analyze', default=False)
		parser.add_argument('--apply_markov_chains', default=False)

	def handle(self, *args, **options):
		file_name = ""
		if options['file_name']:
			file_name = options['file_name']
			setences = utils.read_source_into_sentence_list(file_name)
			author = Person.objects.get_or_create(real_name=options['author'])
			for sentence in sentences: 
				Sentence.create(author=author, content=" ".join(sentence))
			
