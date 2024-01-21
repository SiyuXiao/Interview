import torch
import torch.nn as nn
import torch.optim as optim
import pickle
import numpy as np


class Transformer(object):

	def __init__(self, path):
		with open(path, 'rb') as f:
			self.embedding = pickle.load(f)

	def __call__(self, sentence):
		input = []
		for word in sentence:
			try:
				input.append(self.embedding[word])
			except Exception as e:
				input.append(self.embedding['</s>'])
		input = np.array(input, dtype=np.float32)
		return sentence, input


class Dataset(object):
	
	def __init__(self, path, transformer):
		with open('{}'.format(path), 'rb') as f:
			self.dataset = pickle.load(f)
		self.transformer = transformer

	def __getitem__(self, index):
		sentence = self.dataset[index]
		return self.transformer(sentence)

	def __len__(self):
		return len(self.dataset)


class Dataloader(object):

	def __init__(self, dataset, shuffle, batch_size, drop_last):
		self.dataset = dataset
		self.shuffle = shuffle
		self.batch_size = batch_size
		self.drop_last = drop_last

	def __iter__(self):
		return next(self)

	def __next__(self):
		sentences = []
		inputs = []
		if self.shuffle:
			index_iterator = iter(np.random.permutation(len(self.dataset)))
		else:
			index_iterator = iter(np.arange(len(self.dataset)))
		for index in index_iterator:
			sentence, input = self.dataset[index]
			sentences.append(sentence)
			inputs.append(input)
			if len(inputs) == self.batch_size:
				yield sentences, inputs
				sentences = []
				inputs = []
		if len(inputs) > 0 and not self.drop_last:
			yield sentences, inputs

	def __len__(self):
		if self.drop_last:
			return len(self.dataset) // self.batch_size
		else:
			return (len(self.dataset) + self.batch_size - 1) // self.batch_size


class Model(nn.Module):

	def __init__(self):
		super(Model, self).__init__()
		self.f1 = nn.GRUCell(input_size=128, hidden_size=128, bias=True)
		self.f2 = nn.Linear(in_features=128, out_features=1, bias=True)

	def forward(self, initial_h, input):
		h = initial_h
		for x in input:
			h = self.f1(x, h)
		y = self.f2(h)
		return y


def testing(epoch_number):
	model = Model()
	model.load_state_dict(torch.load('parameters/epoch[{:d}]'.format(epoch_number)))
	transformer = Transformer(path='dataset/preprocessed/embedding')
	test_positive_dataset = Dataset(path='dataset/preprocessed/test/positive_sentences', transformer=transformer)
	test_negative_dataset = Dataset(path='dataset/preprocessed/test/negative_sentences', transformer=transformer)
	test_positive_dataloader = Dataloader(dataset=test_positive_dataset, batch_size=1, shuffle=False, drop_last=False)
	test_negative_dataloader = Dataloader(dataset=test_negative_dataset, batch_size=1, shuffle=False, drop_last=False)
	print('Testing')
	correct_number = 0
	total_number = 0
	incorrect_samples = []
	with torch.no_grad():
		for batch_number, (positive_sentences, positive_inputs) in enumerate(test_positive_dataloader, start=1):
			for sentence, input in zip(positive_sentences, positive_inputs):
				input = input.reshape(1, -1, 128).transpose(1, 0, 2)
				input = torch.from_numpy(input)
				initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
				output = model.forward(initial_h, input)
				output = output.view(-1, )
				output = output.data.cpu().numpy()
				total_number += 1
				if output >= 0.5:
					correct_number += 1
				if output < 0.5:
					incorrect_samples.append(sentence)
			print('{:.2%}'.format(batch_number / (len(test_positive_dataloader) + len(test_negative_dataloader))), end='\r')
		for batch_number, (negative_sentences, negative_inputs) in enumerate(test_negative_dataloader, start=1):
			for sentence, input in zip(negative_sentences, negative_inputs):
				input = input.reshape(1, -1, 128).transpose(1, 0, 2)
				input = torch.from_numpy(input)
				initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
				output = model.forward(initial_h, input)
				output = output.view(-1, )
				output = output.data.cpu().numpy()
				total_number += 1
				if output >= 0.5:
					incorrect_samples.append(sentence)
				if output < 0.5:
					correct_number += 1
			print('{:.2%}'.format((len(test_positive_dataloader) + batch_number) / (len(test_positive_dataloader) + len(test_negative_dataloader))), end='\r')
	with open('incorrect_samples.txt', 'wb') as f:
		for incorrect_sample in incorrect_samples:
			line = '{}\n'.format(''.join(incorrect_sample))
			line = line.encode('utf-8')
			f.write(line)
	print('Accuracy {:.2%}'.format(correct_number / total_number))


if __name__ == '__main__':

	
	testing(epoch_number=3)
