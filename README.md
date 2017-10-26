# LSTM
playground


## Ref

Dataset: https://www.kaggle.com/snap/amazon-fine-food-reviews

LSTM w/ Reddit comments: https://cs224d.stanford.edu/reports/Chavez.pdf

宋睿华：好玩的文本生成 http://www.msra.cn/zh-cn/news/features/ruihua-song-20161226

理解LSTM/RNN中的Attention机制 http://www.jeyzhang.com/understand-attention-in-rnn.html

深度学习在文本简化方面有什么最新应用进展？ https://www.leiphone.com/news/201612/KObxTdB6hvnfiSOc.html

CS224d: Deep Learning for Natural Language Processing http://cs224d.stanford.edu/

```
# macOS
ssh -R 52698:localhost:52698 -i "davidlau-aws-gpu.pem" ubuntu@ec2-52-199-230-98.ap-northeast-1.compute.amazonaws.com

# AWS Deeplearning Ubuntu 16.04 64bit
sudo wget -O /usr/local/bin/rsub \https://raw.github.com/aurora/rmate/master/rmate
sudo chmod a+x /usr/local/bin/rsub
sudo pip3 install --upgrade keras
sudo apt-get install python3-tk

git clone https://github.com/liuslevis/LSTM
cd LSTM
rsub main.py

ipython3 main.py
```
