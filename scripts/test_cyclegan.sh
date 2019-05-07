set -ex
python test.py --dataroot ./datasets/horse2zebra/testA --name horse2zebra_pretrained --model cycle_gan --phase test --no_dropout
