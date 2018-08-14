#!/bin/bash

#gcloud auth activate-service-account --key-file=/var/secrets/evaluation/key.json

echo "Cloud-Building evaluation image"
cd /infrastructure/evaluation
#gcloud builds submit --config cloud_build.yaml

echo "Create evaluation jobs with the nightly dataset list."
while [[ true ]]; do
  #statements
  echo "I'm alive"
  sleep 10
done
#python k8s_job_creator/k8s_job_creator.py --running_in_cluster --dataset_list dataset_lists/nightly_evaluation.csv --docker_image eval_nightly:latest --tags nightly-`date -I` --service_secret=/var/secrets/evaluation/key.json
