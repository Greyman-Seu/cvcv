import torch
import sys
sys.path.insert(0, "tuturial/dl/model/attention_is_all_you_need/code")

# from code.transformer.Models import Transformer
from tuturial.dl.model.attention_is_all_you_need.code.transformer.Models import Transformer

# 模型参数 from chatgpt
batch_size = 5

# n_src_vocab (源语言词汇大小): 源语言（例如英语）的词汇表中唯一词汇的数量。
n_src_vocab = 10000

# n_trg_vocab (目标语言词汇大小): 目标语言（例如法语）的词汇表中唯一词汇的数量。
n_trg_vocab = n_src_vocab

# d_word_vec (词嵌入维度): 模型中词嵌入的维度，即将每个词映射到的向量的大小。
d_word_vec = 512

# d_model (模型维度): Transformer模型的主要维度，决定了模型中隐藏层的大小。
d_model = 512

# d_inner (内部维度): 在Transformer的前馈神经网络（Feedforward Neural Network）中使用的隐藏层的大小。
d_inner = 2048

# n_layers (层数): Transformer模型的层数，即编码器和解码器中堆叠的层数。
n_layers = 6

# n_head (多头注意力头数): 多头自注意力机制中的注意力头的数量。
n_head = 8

# d_k (注意力头的维度): 注意力头中每个键（key）的维度。
d_k = 64

# d_v (注意力头的值的维度): 注意力头中每个值（value）的维度。
d_v = 64

# dropout (Dropout概率): 在模型训练时用于防止过拟合的Dropout概率。
dropout = 0.1

# n_position (位置编码的最大位置): 位置编码中用于表示序列位置的最大位置。
n_position = 200

# src_pad_idx (源语言填充标记的索引): 用于表示源语言中填充标记的索引，通常为0。也就是说如果里面有0，认为是填充上的。
src_pad_idx = 0

# trg_pad_idx (目标语言填充标记的索引): 用于表示目标语言中填充标记的索引，通常为0。
trg_pad_idx = 0


# 初始化Transformer模型
model = Transformer( # emb_src_trg_weight_sharing 由于设置成了共享参数，所以n_src, n_trg需要设置成一样的
    n_src_vocab=n_src_vocab,
    n_trg_vocab=n_trg_vocab,
    src_pad_idx=src_pad_idx,
    trg_pad_idx=trg_pad_idx,
    d_word_vec=d_word_vec,
    d_model=d_model,
    d_inner=d_inner,
    n_layers=n_layers,
    n_head=n_head,
    d_k=d_k,
    d_v=d_v,
    dropout=dropout,
    n_position=n_position
)

# 随机生成一些训练数据（实际应使用您的数据）
src_seq = torch.randint(0, n_src_vocab, (batch_size, 10))  # (batch_size, sequence_length)
trg_seq = torch.randint(0, n_trg_vocab, (batch_size, 12))  # (batch_size, sequence_length)


# 前向传播
output_logits = model(src_seq, trg_seq)
print("Output Logits Shape:", output_logits.shape)
print(model)
