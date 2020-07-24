import requests
import yaml
import json

url = 'https://ne.openpai.org/rest-server/api/v2/jobs'

with open('examples/token.txt', 'r') as file:
    auth_token = file.read()

headers = {'Authorization': 'Bearer ' + auth_token, 'Content-Type': 'text/plain'}

def submit_job(prefix, model, pruner, sparsity, pretrain_epochs, fine_tune_epochs, dataset='cifar10'):
    with open("examples/auto_pruners_torch_pai_ne_template.yml", 'r') as stream:
        job_config = yaml.safe_load(stream)

    commands = "- apt update \
    - apt install -y nfs-common \
    - mkdir /mnt/confignfs-data \
    - mount -t nfs 10.151.40.40:/data/ /mnt/confignfs-data \
    - git clone https://github.com/suiguoxin/pruning-exp-nni/ \
    - python3 -m pip install tensorboard thop \
    - cd pruning-exp-nni && python3 examples/auto_pruners_torch.py \
      --model {model} \
      --dataset {dataset} \
      --load-pretrained-model True \
      --pretrain-epochs {pretrain_epochs} \
      --pretrained-model-dir /mnt/confignfs-data/sgx/experiment_data/{dataset}/{model}/L1FilterPruner/01/model_trained.pth \
      --pruner {pruner} --base-algo l1 --cool-down-rate 0.9 \
      --sparsity {sparsity} \
      --speed-up True \
      --fine-tune True --fine-tune-epochs {fine_tune_epochs} \
      --data-dir /mnt/confignfs-data/sgx/{dataset} \
      --experiment-data-dir /mnt/confignfs-data/sgx/experiment_data/{dataset}/{model}/{pruner}/{sparsity_str}".format(
          dataset=dataset, model=model, pruner=pruner, sparsity=sparsity, sparsity_str=str(sparsity).replace('.', ''), pretrain_epochs=pretrain_epochs, fine_tune_epochs=fine_tune_epochs)
    
    job_config["taskRoles"]["taskrole"]["commands"] = commands.split('- ')
    job_config["name"] = "{prefix}_{model}_{dataset}_{pruner}_{sparsity_str}".format(prefix=prefix, dataset=dataset, model=model, pruner=pruner, sparsity=sparsity, sparsity_str=str(sparsity).replace('.', ''))

    print(yaml.dump(job_config))
    r = requests.post(url, headers=headers, data=yaml.dump(job_config))
    print(r.text)


if __name__ == '__main__':
    # models = ['vgg16']
    # pruners = ['SimulatedAnnealingPruner']
    # sparsities = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.95', '0.975']
    # for model in models:
    #     for pruner in pruners:
    #         for sparsity in sparsities:
    #             submit_job('_0724', model, pruner, sparsity, pretrain_epochs=100, fine_tune_epochs=100)

    models = ['resnet18']
    pruners = ['SimulatedAnnealingPruner']#'ActivationMeanRankFilterPruner', 'ActivationAPoZRankFilterPruner']#'L1FilterPruner', , 'NetAdaptPruner', 'AutoCompressPruner']
    sparsities = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.95', '0.975']
    for model in models:
        for pruner in pruners:
            for sparsity in sparsities:
                submit_job('_0724', model, pruner, sparsity, pretrain_epochs=200, fine_tune_epochs=200)

    # models = ['resnet50']
    # pruners = ['L1FilterPruner']
    # sparsities = ['0.1', '0.975']
    # for model in models:
    #     for pruner in pruners:
    #         for sparsity in sparsities:
    #             submit_job('0723', model, pruner, sparsity, fine_tune_epochs=200)
    
    # # prepare pretrained models
    # models = ['resnet18', 'vgg16']
    # pruners = ['L1FilterPruner']
    # sparsities = ['0.1']
    # for model in models:
    #     for pruner in pruners:
    #         for sparsity in sparsities:
    #             submit_job(model, pruner, sparsity)
