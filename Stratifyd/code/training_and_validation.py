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
		return input


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
		batch = []
		if self.shuffle:
			index_iterator = iter(np.random.permutation(len(self.dataset)))
		else:
			index_iterator = iter(np.arange(len(self.dataset)))
		for index in index_iterator:
			sentence = self.dataset[index]
			batch.append(sentence)
			if len(batch) == self.batch_size:
				yield batch
				batch = []
		if len(batch) > 0 and not self.drop_last:
			yield batch

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


def training_and_validation(start_epoch_number, end_epoch_number):
	model = Model()
	if start_epoch_number > 1:
		model.load_state_dict(torch.load('parameters/epoch[{:d}]'.format(start_epoch_number-1)))
	criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor(data=[1], dtype=torch.float32))
	optimizer = optim.Adam(params=model.parameters(), lr=1e-3, betas=(0.9, 0.999), amsgrad=True)
	transformer = Transformer(path='dataset/preprocessed/embedding')
	train_positive_dataset = Dataset(path='dataset/preprocessed/train/positive_sentences', transformer=transformer)
	train_negative_dataset = Dataset(path='dataset/preprocessed/train/negative_sentences', transformer=transformer)
	valid_positive_dataset = Dataset(path='dataset/preprocessed/valid/positive_sentences', transformer=transformer)
	valid_negative_dataset = Dataset(path='dataset/preprocessed/valid/negative_sentences', transformer=transformer)
	train_positive_dataloader = Dataloader(dataset=train_positive_dataset, batch_size=1, shuffle=True, drop_last=True)
	train_negative_dataloader = Dataloader(dataset=train_negative_dataset, batch_size=1, shuffle=True, drop_last=True)
	valid_positive_dataloader = Dataloader(dataset=valid_positive_dataset, batch_size=100, shuffle=False, drop_last=True)
	valid_negative_dataloader = Dataloader(dataset=valid_negative_dataset, batch_size=100, shuffle=False, drop_last=True)
	print('Training and Validation')
	for epoch_number in range(start_epoch_number, end_epoch_number+1):
		print('Epoch {:d}'.format(epoch_number))
		epoch_loss = []
		for batch_number, (positive_inputs, negative_inputs) in enumerate(zip(train_positive_dataloader, train_negative_dataloader), start=1):
			model.zero_grad()
			positive_outputs = []
			for input in positive_inputs:
				input = input.reshape(1, -1, 128).transpose(1, 0, 2)
				input = torch.from_numpy(input)
				initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
				output = model.forward(initial_h, input)
				output = output.view(-1, )
				positive_outputs.append(output)
			positive_outputs = torch.stack(positive_outputs, 0)
			negative_outputs = []
			for input in negative_inputs:
				input = input.reshape(1, -1, 128).transpose(1, 0, 2)
				input = torch.from_numpy(input)
				initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
				output = model.forward(initial_h, input)
				output = output.view(-1, )
				negative_outputs.append(output)
			negative_outputs = torch.stack(negative_outputs, 0)
			T = torch.ones(size=(1, 1), dtype=torch.float32)
			F = torch.zeros(size=(1, 1), dtype=torch.float32)
			batch_loss = 0.5 * criterion(positive_outputs, T) + 0.5 * criterion(negative_outputs, F)
			batch_loss.backward()
			optimizer.step()
			batch_loss = batch_loss.data.cpu().numpy()
			epoch_loss.append(batch_loss)
			print('{:.2%}'.format(batch_number / min(len(train_positive_dataloader), len(train_negative_dataloader))), end='\r')
		print('Training Loss {:.5f}'.format(np.mean(epoch_loss)))
		epoch_loss = []
		with torch.no_grad():
			for batch_number, (positive_inputs, negative_inputs) in enumerate(zip(valid_positive_dataloader, valid_negative_dataloader), start=1):
				positive_outputs = []
				for input in positive_inputs:
					input = input.reshape(1, -1, 128).transpose(1, 0, 2)
					input = torch.from_numpy(input)
					initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
					output = model.forward(initial_h, input)
					output = output.view(-1, )
					positive_outputs.append(output)
				positive_outputs = torch.stack(positive_outputs, 0)
				negative_outputs = []
				for input in negative_inputs:
					input = input.reshape(1, -1, 128).transpose(1, 0, 2)
					input = torch.from_numpy(input)
					initial_h = torch.zeros(size=(1, 128), dtype=torch.float32)
					output = model.forward(initial_h, input)
					output = output.view(-1, )
					negative_outputs.append(output)
				negative_outputs = torch.stack(negative_outputs, 0)
				T = torch.ones(size=(100, 1), dtype=torch.float32)
				F = torch.zeros(size=(100, 1), dtype=torch.float32)
				batch_loss = 0.5 * criterion(positive_outputs, T) + 0.5 * criterion(negative_outputs, F)
				batch_loss = batch_loss.data.cpu().numpy()
				epoch_loss.append(batch_loss)
				print('{:.2%}'.format(batch_number / min(len(valid_positive_dataloader), len(valid_negative_dataloader))), end='\r')
		print('Validation Loss {:.5f}'.format(np.mean(epoch_loss)))
		torch.save(model.state_dict(), 'parameters/epoch[{:d}]'.format(epoch_number))


if __name__ == '__main__':

	
	training_and_validation(start_epoch_number=1, end_epoch_number=3)
