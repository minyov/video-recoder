#!/usr/bin/env bash


kubectl delete -f ./nginx/service.yaml
kubectl delete -f ./nginx/deployment.yaml

kubectl delete -f ./api/service.yaml
kubectl delete -f ./api/deployment.yaml

kubectl delete -f ./celery/deployment.yaml

kubectl delete -f ./mq/service.yaml
kubectl delete -f ./mq/deployment.yaml

kubectl delete -f ./db/service.yaml
kubectl delete -f ./db/deployment.yaml

kubectl delete -f ./volumes/django-pvc.yaml
kubectl delete -f ./volumes/django-pv.yaml
kubectl delete -f ./volumes/db-pvc.yaml
kubectl delete -f ./volumes/db-pv.yaml

kubectl delete -f ./api/collectstatic-job.yaml
kubectl delete -f ./api/migration-job.yaml
