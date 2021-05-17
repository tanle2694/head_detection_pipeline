```
    ssh-keyscan github.com > /tmp/known_hosts
```

```
kubectl create secret generic git-creds \
    --from-file=ssh=$HOME/.ssh/id_rsa \
    --from-file=known_hosts=/tmp/known_hosts -n $KUBEFLOW_NAMESPACE
```
