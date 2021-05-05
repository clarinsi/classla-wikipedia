import sys

def patch_conllu(text):
        prev_ner='NER=O'
        curr_ner='NER=O'
        result = []
        for line in text.split('\n'):
                if len(line)>0:
                        if line[0].isdigit():
                                line = line.split('\t')
                                line[5] = '|'.join(sorted(line[5].split('|'), key = lambda x: x.split('=')[0].lower()))
                                if line[7] != '_':
                                        line[7] = line[7].replace('_',':')
                                if line[7] == '<PAD>':
                                        line[7] = 'dep'
                                if line[9].startswith('NER'):
                                        curr_ner = line[9].split('|')[0].strip()
                                if curr_ner.startswith('NER=I-') and not prev_ner.endswith(curr_ner.split('-')[-1]):
                                        line[9] = 'NER=B-' + line[9][6:]
                                prev_ner = curr_ner
                                line = '\t'.join(line)
                result.append(line)
        return '\n'.join(result)

text = ''
for line in sys.stdin:
	text += line
	if line.strip() == '':
		sys.stdout.write(patch_conllu(text))
		text = ''

