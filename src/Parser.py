#PARSER will take in a twiter quote, and assign it an emotional value
#Contains a quoteItem that will be analyzed and have its emotional number changed

import QuoteItem
import nltk
from nltk.chunk import RegexpParser

class Parser:
	quote = ""
	quoteItemCondensedList = []

	'''----------------------------------------------------------------------------------------'''

	def __init__(self, externalQuoteItem):
		'''To hold the original quote as a quote Item object'''
		self.quote = externalQuoteItem.getQuote()

	def parse(self):
		'''Take it a quoteItem, to alter it's values'''
		quoteTokenized = nltk.word_tokenize(self.quote)
		posTaggedQuote = nltk.pos_tag(quoteTokenized)
		self.condense(posTaggedQuote)

	def condense(self, posTaggedQuote):
		'''This will condense the tagged quote by recursively calling the chunk method'''
		self.chunk(posTaggedQuote)

	def chunk(self, posTaggedQuote):
		'''Holds the chunkers used by the condensed class'''
		quoteItemCondensedList = [] 								   #Need to zero this our for testing, might take away later
		EMPChunker = RegexpParser(r"""
		EMP:                                                           #Emotion Phrase
			{<MD>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ><,><CC>}                  #Modular, verb, anything, adjective, comma, conjunction
			{<MD>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ><CC>}                     #Modular, verb, anything, adjective, conjunction
			{(<VBP>|<VB>|<VBZ>|<VBD>)<JJ><,><CC>}                      #Verb, anything, adjective, comma, conjunction
		    {(<VBP>|<VB>|<VBZ>|<VBD>)<JJ><CC>}                         #Verb, anything, adjective, conjunction

		    {(<VBP>|<VB>|<VBZ>|<VBD>)<JJ><CC>}	                       #Verb, anything, adjective, conjunction

			{(<VBP>|<VB>|<VBZ>|<VBD>)<RB><JJ>}                         #Verb, adverb, adjective
		   	{<MD><RB>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ>}                     #Modular, adverb, verb, adjective
			{<RB>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ>}                         #Adverb, verb, adjective

			{<MD>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ>}                         #Modular, verb, anything, adjective
			{(<VBP>|<VB>|<VBZ>|<VBD>)<TO>(<VBP>|<VB>|<VBZ>|<VBD>)<JJ>} #Verb, "to", verb anything, adjective
			{(<VBP>|<VB>|<VBZ>|<VBD>)<JJ>}                             #Verb, anything, adjective

		""")
		PRPHChunker = RegexpParser(r"""
		PRPH:                                                          #Preposition Phrase
			{<.*>*<PRP><.*>*<EMP>}				                       #Anything, proposition, anything
			{<EMP><.*>*<PRP><.*>*}				                       #Anything, proposition, anything
			}<EMP>{													   #Chink at the EMP chunk, recursion!
		""")

		#This is going to have to be recursive, to chunk the entire phrase
		#This section chunkes, and condenses, the EMP chunk becomes "EMP"
		#Then sets the happy level of the condesned quoteItem
		EMPChunked = EMPChunker.parse(posTaggedQuote)
		for piece in EMPChunked:
			if type(piece) != tuple:
				#self.quoteItemCondensedList.append((piece, 'EMP'))			#TESTING
				self.quoteItemCondensedList.append(('','EMP'))			#TESTING
			else:
				self.quoteItemCondensedList.append(piece)
		self.printCondensed()


		#Simulating the recursion, PRP chunk next
		#Want to chunk everything seperately, then figure out the best recursive algorithm
		newQuoteItemCondensedList = self.quoteItemCondensedList
		self.quoteItemCondensedList = []									#Clear the list to condense more
		PRPHChunked = PRPHChunker.parse(newQuoteItemCondensedList)
		for piece in PRPHChunked:
			if type(piece) != tuple:
				#self.quoteItemCondensedList.append((piece, 'PRPH'))		#TESTING
				self.quoteItemCondensedList.append(('','PRPH'))				#TESTING
			else:
				self.quoteItemCondensedList.append(piece)
		self.printCondensed()

		newQuoteItemCondensedList = self.quoteItemCondensedList
		self.quoteItemCondensedList = []									#Clear the list to condense more
		PRPHChunked = PRPHChunker.parse(newQuoteItemCondensedList)
		for piece in PRPHChunked:
			if type(piece) != tuple:
				#self.quoteItemCondensedList.append((piece, 'PRPH'))		#TESTING
				self.quoteItemCondensedList.append(('','PRPH'))				#TESTING
			else:
				self.quoteItemCondensedList.append(piece)
		self.printCondensed()

		#self.quoteItemCondensed.setValue(1)  						#This line, or a variant will be moved eventually, and will have to be an average

	def printCondensed(self):
		#For testing
		print "The quote chunked and parsed:"
		print self.quoteItemCondensedList
		print "\n"


















