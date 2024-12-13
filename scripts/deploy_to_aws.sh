#!/bin/sh

TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition "$TASK_DEFINITION_NAME"  --query taskDefinition --output json)
echo "$TASK_DEFINITION" > prev_task_definition.json
NEW_TASK_DEFINITION=$(jq --compact-output --arg IMAGE "podemosprogresar/$SERVICE_IMAGE:$CI_COMMIT_SHORT_SHA" '.containerDefinitions[0].image = $IMAGE | del( .compatibilities, .taskDefinitionArn, .requiresAttributes, .revision, .status, .registeredAt, .deregisteredAt, .registeredBy )' prev_task_definition.json)
echo "$NEW_TASK_DEFINITION" > new_task_definition.json
NEW_TASK_DEFINITION_ARN=$(aws ecs register-task-definition --execution-role-arn ${AWS_EXECUTION_ROLE_ARN} --cli-input-json file://new_task_definition.json --query taskDefinition.taskDefinitionArn --output text)
APPSPEC_JSON=$(jq --compact-output --arg TASK_DEFINITION_ARN $NEW_TASK_DEFINITION_ARN --arg CONTAINER_NAME $CONTAINER_NAME '.Resources[0].TargetService.Properties.TaskDefinition = $TASK_DEFINITION_ARN | .Resources[0].TargetService.Properties.LoadBalancerInfo.ContainerName = $CONTAINER_NAME' infrastructure/appspec.json)
echo "$APPSPEC_JSON" > appspec.json
DEPLOYMENT_ID=$(aws deploy create-deployment --query deploymentId --output text --application-name $APPLICATION_NAME --deployment-group-name $DEPLOYMENT_GROUP_NAME --revision revisionType=AppSpecContent,appSpecContent={content="'$(cat appspec.json)'"})
