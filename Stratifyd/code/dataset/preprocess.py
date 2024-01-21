import os
import jieba
import pickle
import word2vec
import numpy as np


def preprocess():
	if not os.path.exists('preprocessed'):
		os.mkdir('preprocessed')
		os.mkdir('preprocessed/train')
		os.mkdir('preprocessed/valid')
		os.mkdir('preprocessed/test')

		sentences = []

		positive_sentences = []
		negative_sentences = []

		train_positive_sentences = []
		valid_positive_sentences = []
		test_positive_sentences = []

		train_negative_sentences = []
		valid_negative_sentences = []
		test_negative_sentences = []
		
		with open('original/pos.txt', 'rb') as f:
			for line in f:
				try:
					line = line.decode('utf-8')
					line = line.rstrip()
					if line in ['na', '没有描述']:
						continue
					line = list(jieba.cut(line))
					sentences.append(line)
					positive_sentences.append(line)
				except Exception as e:
					pass
		
		with open('original/neg.txt', 'rb') as f:
			for index, line in enumerate(f):
				try:
					line = line.decode('utf-8')
					line = line.rstrip()
					if line in ['na', '没有描述']:
						continue
					line = list(jieba.cut(line))
					sentences.append(line)
					negative_sentences.append(line)
				except Exception as e:
					pass

		with open('original/separated-by-space', 'wb') as f:
			for sentence in sentences:
				line = '{}\n'.format(' '.join(sentence))
				line = line.encode('utf-8')
				f.write(line)
		
		word2vec.word2vec(train='original/separated-by-space',
		                  output='preprocessed/embedding.bin',
		                  size=128,
		                  window=20,
		                  sample='1e-3',
		                  hs=1,
		                  negative=5,
		                  threads=10,
		                  iter_=5,
		                  min_count=5,
		                  alpha=0.025,
		                  debug=2,
		                  binary=1,
		                  cbow=0,
		                  save_vocab=None,
		                  read_vocab=None,
		                  verbose=False)
		
		model = word2vec.load('preprocessed/embedding.bin')
		embedding = {word: model[word] for word in model.vocab}
		with open('preprocessed/embedding', 'wb') as f:
			pickle.dump(embedding, f)
		
		os.remove('original/separated-by-space')
		os.remove('preprocessed/embedding.bin')

		np.random.shuffle(positive_sentences)
		for index, sentence in enumerate(positive_sentences):
			if index % 10 == 0:
				test_positive_sentences.append(sentence)
			elif index % 10 == 1:
				valid_positive_sentences.append(sentence)
			else:
				train_positive_sentences.append(sentence)


		np.random.shuffle(negative_sentences)
		for index, sentence in enumerate(negative_sentences):
			if index % 10 == 0:
				test_negative_sentences.append(sentence)
			elif index % 10 == 1:
				valid_negative_sentences.append(sentence)
			else:
				train_negative_sentences.append(sentence)

		# len(train_positive_sentences) = 80000
		# len(train_negative_sentences) = 160000
		# len(valid_positive_sentences) = 10000
		# len(valid_negative_sentences) = 20000
		# len(test_positive_sentences) = 10000
		# len(test_negative_sentences) = 20000

		train_positive_sentences = train_positive_sentences * 2
		valid_positive_sentences = valid_positive_sentences * 2

		with open('preprocessed/train/positive_sentences', 'wb') as f:
			pickle.dump(train_positive_sentences, f)
		with open('preprocessed/valid/positive_sentences', 'wb') as f:
			pickle.dump(valid_positive_sentences, f)
		with open('preprocessed/test/positive_sentences', 'wb') as f:
			pickle.dump(test_positive_sentences, f)

		with open('preprocessed/train/negative_sentences', 'wb') as f:
			pickle.dump(train_negative_sentences, f)
		with open('preprocessed/valid/negative_sentences', 'wb') as f:
			pickle.dump(valid_negative_sentences, f)
		with open('preprocessed/test/negative_sentences', 'wb') as f:
			pickle.dump(test_negative_sentences, f)


def test():
	with open('preprocessed/embedding', 'rb') as f:
		embedding = pickle.load(f)
	cosine_function = lambda v1, v2: np.dot(v1, v2) / (np.sqrt(np.sum(v1 ** 2)) * np.sqrt(np.sum(v2 ** 2)))
	similar_words = [[word, cosine_function(embedding['贵'], embedding[word])] for word in embedding.keys()]
	similar_words.sort(key=lambda x: x[1], reverse=True)
	for word, cosine in similar_words[:10]:
		print(word, cosine)


if __name__ == '__main__':

	
	preprocess()
	test()
	