docker build -t gusui/nni:autopruners . --no-cache

docker push gusui/nni:autopruners

scp -r core@10.151.40.40:/data/share/drbdha/data/sgx/experiment_data/cifar10/vgg16/ experiment_data/cifar10

rsync -avzh --exclude '*.pth' core@10.151.40.40:/data/share/drbdha/data/sgx/experiment_data/cifar10/ experiment_data/cifar10
