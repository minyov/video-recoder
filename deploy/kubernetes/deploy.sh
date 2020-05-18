#!/usr/bin/env bash

kubectl apply -f ./secrets.yaml

kubectl apply -f ./volumes/db-pv.yaml
kubectl apply -f ./volumes/db-pvc.yaml
kubectl apply -f ./volumes/django-pv.yaml
kubectl apply -f ./volumes/django-pvc.yaml

kubectl apply -f ./db/deployment.yaml
kubectl apply -f ./db/service.yaml

kubectl apply -f ./api/collectstatic-job.yaml
kubectl apply -f ./api/migration-job.yaml

kubectl apply -f ./mq/deployment.yaml
kubectl apply -f ./mq/service.yaml

kubectl apply -f ./celery/deployment.yaml

kubectl apply -f ./api/deployment.yaml
kubectl apply -f ./api/service.yaml

kubectl apply -f ./nginx/deployment.yaml
kubectl apply -f ./nginx/service.yaml

kubectl apply -f ./ingress.yaml
