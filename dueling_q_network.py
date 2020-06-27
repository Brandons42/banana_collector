import torch
import torch.nn as nn
import torch.nn.functional as F

class DuelingQNetwork(nn.Module):
	def __init__(self, state_size, action_size, seed, fc1_units=16, fc2_units=16, val_stream_units=16, adv_stream_units=16):
		super(DuelingQNetwork, self).__init__()
		self.seed = torch.manual_seed(seed)
		self.fc1 = nn.Linear(state_size, fc1_units)
		self.fc2 = nn.Linear(fc1_units, fc2_units)

		# Value function stream
		self.val_stream_fc1 = nn.Linear(fc2_units, val_stream_units)
		self.val_stream_fc2 = nn.Linear(val_stream_units, 1)

		# Advantage function stream
		self.adv_stream_fc1 = nn.Linear(fc2_units, adv_stream_units)
		self.adv_stream_fc2 = nn.Linear(adv_stream_units, action_size)
	def forward(self, state):
		x = F.relu(self.fc1(state))
		x = F.relu(self.fc2(x))

		y = F.relu(self.val_stream_fc1(x))
		y = F.relu(self.val_stream_fc2(y))

		z = F.relu(self.adv_stream_fc1(x))
		z = self.adv_stream_fc2(z)

		return y + (z - z.mean())