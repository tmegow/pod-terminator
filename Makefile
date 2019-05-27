repo=pod-terminator
shorthash=`git rev-parse --short HEAD`
base=tmegow/$(repo)
image=$(base):$(shorthash)

all: build-image template-k8s-manifests

build-image:
	docker build -t $(image) .
	docker tag $(image) $(base):latest

template:
	ansible-playbook ansible/tasks/main.yaml
