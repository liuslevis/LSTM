# LSTM
playground

Dataset: https://www.kaggle.com/snap/amazon-fine-food-reviews

```
# macOS

ssh -R 52698:localhost:52698 -i "davidlau-aws-gpu.pem" ubuntu@ubuntu@ec2-13-115-82-114.ap-northeast-1.compute.amazonaws.com

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
