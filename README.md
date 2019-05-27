# pod-terminator

Deletes pods at intervals

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
