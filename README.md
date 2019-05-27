# pod-terminator

Deletes kubernetes pods by selector at chosen intervals 

## Configuration

The [vars file](https://github.com/tmegow/pod-terminator/blob/master/k8s/vars/main.yaml) contains a list of dictionaries, `targets`. `targets` entries contain 3 sub-keys:
* Selector - (dict) selector string values (supports multiple)
* namespace - (str) target namespace
* interval - (str or int) int values are accepted as seconds values. Strings ending in `s`,`m`,`h`,`d` for specifying interval times are accepted.
_Remember to modify the example deletion schedules configured in the [vars file](https://github.com/tmegow/pod-terminator/blob/master/k8s/vars/main.yaml) with custom deletion schedules_

### Example
```
config:
  targets:
    - selector:
        app: "hello-kubernetes"
      namespace: "default"
      interval: "3h"
    - selector:
        name: "nginx"
        app: "data-sync"
      namespace: "data-sync"
      interval: "1d"
```
### Usage
* Install python requirements from requirements.txt file
  * `virtualenv .venv; pip install -r requirements.txt`
* Run make "all" target to create docker container and template k8s manifests
  * `make all`
* Review and apply k8s manifests
  * `kubectl apply -f tmp-k8s/ #Example output below`

```bash
$ kubectl apply -f tmp-k8s/
 clusterrole.rbac.authorization.k8s.io/delete-pods created
 clusterrolebinding.rbac.authorization.k8s.io/pod-terminator created
 configmap/pod-terminator created
 deployment.apps/pod-terminator created
 serviceaccount/pod-terminator created
```
