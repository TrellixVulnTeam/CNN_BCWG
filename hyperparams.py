import torch
import random
torch.manual_seed(121)
random.seed(121)

learning_rate = 0.001
epochs = 256
batch_size = 16
log_interval = 1
test_interval = 10000
save_interval = 100
save_dir = "snapshot"
datafile_path = "./data/"
name_trainfile = "raw.clean.train"
name_devfile = "raw.clean.dev"
name_testfile = "raw.clean.test"
word_data = False
char_data = False
shuffle = True
epochs_shuffle = True
FIVE_CLASS_TASK = False
TWO_CLASS_TASK = True
dropout = 0.6
max_norm = 5
clip_max_norm = 3
# clip_max_norm
kernel_num = 200
# kernel_sizes = "7,8,9,10"
# kernel_sizes = "7,7,7"
kernel_sizes = "1,2,3,4"
static = False
CNN = True
CNN_MUI = False
DEEP_CNN = False
LSTM = False
GRU = False
BiLSTM = False
BiLSTM_1 = False
CNN_LSTM = False
CNN_BiLSTM = False
CLSTM = False
CBiLSTM = False
CGRU = False
BiGRU = False
CNN_BiGRU = False
# select optim algorhtim to train
Adam = True
SGD = False
Adadelta = False
optim_momentum_value = 0.9
# whether to use wide convcolution True : wide  False : narrow
wide_conv = True
# whether to use batch normalizations
batch_normalizations = False
bath_norm_momentum = 0.1   # default is 0.1
batch_norm_affine = False  # default is True
# min freq to include during built the vocab, default is 1
min_freq = 1
# word_Embedding
word_Embedding = True
embed_dim = 300
word_Embedding_Path = "./word2vec/glove.sentiment.conj.pretrained.txt"
# word_Embedding_Path = "./word2vec/glove.semeval.conj.pretrained.txt"
# word_Embedding_Path = "./word2vec/w2v103100-en.100d.txt"
lstm_hidden_dim = 100
lstm_num_layers = 1
device = -1
no_cuda = False
snapshot = None
predict = None
test = False
num_threads = 1
freq_1_unk = False
# whether to init w
init_weight = True
init_weight_value = 2.0
# L2 weight_decay
weight_decay = 1e-8   # default value is zero in Adam SGD
# weight_decay = 0   # default value is zero in Adam SGD
# random seed
seed_num = 222
# whether to delete the model after test acc so that to save space
rm_model = True



