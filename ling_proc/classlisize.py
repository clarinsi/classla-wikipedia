import sys
wiki = sys.argv[1]
if wiki == 'sr':
	from serbian import srSplitDigraphs,srCyrillicToLatin
import unicodedata
import os
import classla
import re
url_re = re.compile('url="(.+?)"')
title_re = re.compile('title="(.+?)"')
id_re = re.compile('id="(.+?)"')
space_re = re.compile('\s+',re.UNICODE)

def cleanup(text):
	newtext = ''
	text = space_re.sub(' ', text)
	for char in text:
		if char == '\u00a0':
			newtext += '\u0020'
		elif char == '\u2011':
			newtext += '\u002d'
		elif char != '\u00ad':
			newtext += char
	return unicodedata.normalize('NFKC', newtext)

def cyr_to_lat(text):
	return srSplitDigraphs(srCyrillicToLatin(text))

def enrich_ids(text, doc_id):
	result = []
	for line in text.split('\n'):
		if line.startswith('# newpar id =') or line.startswith('# sent_id ='):
			line = line.split(' = ')
			result.append(line[0] + ' = ' + doc_id + '.' + line[1])
		else:
			result.append(line)
	return '\n'.join(result)

lang = {'bg': 'bg','bs':'hr','sh':'hr','sr':'sr','hr':'hr','mk':'mk','sl':'sl'}[wiki]

nlp = classla.Pipeline(lang)

f=open(wiki+'.prelim.conllu', 'w')

for root, subdirs, files in os.walk('../output/' + wiki):
	for filename in files:
		file_path = os.path.join(root, filename)
		text = ''
		for line in open(file_path):
			if line.startswith('<doc'):
				skip = False
				text = ''
				try:
					doc_id = 'classlawiki-' + wiki + '.' + id_re.search(line).group(1)
				except:
					print('issue with id',line)
					skip = True
				try:
					doc_url = url_re.search(line).group(1)
				except:
					print('issue with url',line)
					skip = True
				try:
					doc_title = title_re.search(line).group(1)
				except:
					print('issue with title',line)
					skip = True
				if lang == 'sr':
					doc_title = cyr_to_lat(doc_title)
				if not skip:
					proc_text = '# newdoc id = ' + doc_id + '\n'
					proc_text += '# url = ' + doc_url+ '\n'
					proc_text += '# title = ' + doc_title + '\n'
			elif line.startswith('<section'):
				try:
					title = title_re.search(line).group(1)
				except:
					print('section without title',line)
					title = ''
				if title != '':
					text += title + '\n'
			elif line.startswith('<formula'):
				continue
			elif line.startswith('</doc'):
				if skip:
					text = ''
					continue
				try:
					doc = nlp(text.strip())
				except:
					text = ''
					print('memory error')
					continue
				proc_text += enrich_ids(doc.to_conll(), doc_id)
				f.write(proc_text)
				text = ''
			elif line.strip() != '':
				if lang == 'sr':
					text += cyr_to_lat(line)
				else:
					text += line
f.close()
