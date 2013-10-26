#oop stuffs from http://www.tutorialspoint.com/python/python_classes_objects.htm


#read in somehow
	#from pointer file for now
#regular expression out:
	#first line: title
	#last sentance of first paragraph: THesis! (maybe)
	#first sentance of subsequent paragraphs: TS
	#andything before (words numbers): support

#later: 
	#allow to view evidence by source ie show everything they took from that source
		#would be helpful for annotated biblios, etc
		#would need to isolate the last names of authors
		#then search through all the pieces of evidence, recording when found
	#mark things in essay to organize later
	#once digested, allow user to adjust that their "thesis" is, etc?
	#go from outline to text format?

#MUCH later
	#read from google docs?
		#would need permissions, etc.
	#read from pdf?
		#would need image->text
	#read from jstor?
		#would prob need from pdf & crawling stuffs

import os;
import re;

#get an esasy to digest-- for now I've hard coded this one. 
os.chdir("/Users/m13hall/Documents/Other")
s = open("sampleEssay.txt");
strEssay = s.read();
#################
#purpose: finds any evidence 
def findEvidence(body):
	evidence = [];
	for line in body:
		ev = re.findall("([^.]+\([^\)]+[0-9]+\))", line);
		if ev is not []:
			for piece in ev:
				evidence.append(piece);
	return evidence;


##OOP
#general paragraph format
#the signifianct parts in a paragraph are the first & last line & the lines in the middle
class paragraph:
	firstLine = '';
	body = '';
	lastLine = '';
	def __init__(self, strParagraph):
		lines = re.findall("([^\.]+\.)", strParagraph);
		self.firstLine = lines[0];
		self.body = lines[1:len(lines)-2];
		self.lastLine = lines[len(lines)-1];
#intro, body, and conclusion paragraphs are just special types of the general paragraph
class intro(paragraph):
	hook = '';
	body = '';
	thesis = '';
	def __init__(self, paragraph):
		self.hook = paragraph.firstLine;
		self.body = paragraph.body;
		self.thesis = paragraph.lastLine;
#body has a special field, the evidence field. this uses regexp to pull out any citations 
class body(paragraph):
	ts = '';
	body = '';
	lastLine = '';
	evidence = [];
	def __init__(self, paragraph):
		self.ts = paragraph.firstLine;
		self.body = paragraph.body;
		self.lastline = paragraph.lastLine;
		self.evidence = findEvidence(paragraph.body);
#conclusion's reThesis should be a restatementish of the original thesis

class conclusion(paragraph):
	reThesis = '';
	body = '';
	lastline = '';
	def __init__(self, paragraph):
		self.reThesis = paragraph.firstLine;
		self.body = paragraph.body;
		self.lastLine = paragraph.lastLine;
#worksCited stores both each entry as a whole (including the authors) 
#and a list with just the authors
class worksCited():
	entries = [];
	authors = [];
	def __init__(self, lsWorksCited):

		self.entries = lsWorksCited[1:];
		self.authors = [re.split('[.](?!,)', x)[0] for x in self.entries];

#this is where most of the parsing happens to go from a essay in string format to an 
#essay object, which contains paragraph objects and a worksCited object
class essay:
	title = '';
	intro = '';
	body = []; #list of paragraphs
	conclusion = '';
	worksCited = '';
	
	def __init__(self, strEssay):
		titleNBody = re.split("\A([^\n]+)\n", strEssay);
		if re.search('\A[\s+]\z', titleNBody[0]) == None:
			titleIndex = 1;
		else:
			titleIndex = 0;
		self.title = titleNBody[titleIndex];
		bodyNWorksCited = titleNBody[titleIndex + 1];
		bodyNWorksCited = bodyNWorksCited.split('\n');
		for i in range(len(bodyNWorksCited)):
			if re.search('\Aworks cited', bodyNWorksCited[i].lower()):
				self.worksCited = worksCited(bodyNWorksCited[i:len(bodyNWorksCited)-1]);
				tempBody = [paragraph(x) for x in bodyNWorksCited[0:i]];
				break;
		endIntroIndex = 0; 
		beginConclusionIndex = len(tempBody)-1;
		self.intro = intro(tempBody[endIntroIndex]);
		self.conclusion = conclusion(tempBody[beginConclusionIndex]);
		self.body = [body(x) for x in tempBody[endIntroIndex:beginConclusionIndex]];
	
	def showSupport(self):
		print 'Thesis:' + self.intro.thesis;
		print 
		for par in self.body:
			print '\t' + par.ts 
			print 'pieces of evidence: '+ str(len(par.evidence))
			for piece in par.evidence:
				print '\t\t' + piece;


	
	

sample = essay(strEssay);

#sample.showSupport();
print sample.worksCited.entries
print sample.worksCited.sources
