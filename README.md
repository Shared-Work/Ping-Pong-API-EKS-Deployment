# Ping-Pong-API-EKS-Deployment



## ***Description:***
It’s required to do the following:

-  Write a ping pong API using any language.

-  Dockrize the API following the best practices.

- Create an EKS cluster.

- Create Kubernetes deployment and service for that ping/pong API.

- Create a helm chart for this ping pong service.

- Bonus:

      - Install Prometheus and configure monitoring metrics.

      - Write IaC files to create the k8s on AWS EKS

## ***Acceptence Criteria:***
 To access ping-pong api deployed on the EKS cluster through service load balancer endpoint.

## ***Steps:***

1- **Create VPC and networking resources:**

Now we need to create VPC and EKS cluster. To create them, navigate to AWS CloudFormation and click on “Create stack” and use **Networking-Stack.yml** template , it will apply the below resources:
 -  VPC
 - Subnets
 - Routetables
 - internet gw
 - nat gw
 - EKS cluster role : that allows Kubernetes to create AWS resources.
 - EKS Cluster

2- Configure kubectl for Amazon EKS.
you can create kubeconfig that you will use to access the cluster.
by default it will created under ~/.kube/config

```
aws eks --region <region> update-kubeconfig --name <clusterName>
```

3- **Create worker nodes to join the Kubernetes cluster:**

- Now we need to create worker nodes to join the Kubernetes cluster. To create them, navigate to AWS CloudFormation and click on “Create stack” and use Nodes-Stack.yml template

- In the next page, you need to fill the required information as below.

   **Stack name**: GIve any unique name to the stack

   **ClusterName**: Give the previously created Kubernetes cluster name

   **ClusterControlPlaneSecurityGroup**: Give the SecurityGroup value obtained from the outputs of networking stack.

    **NodeGroupName**: Give any unique name

    **NodeAutoScalingGroupMinSize**: 2

    **NodeAutoScalingGroupDesiredCapacity**: 2

    **NodeAutoScalingGroupMaxSize**: 3

    **NodeInstanceType** : t3.medium

    **NodeImageId**: Give a suitable Node image ID using the below link:
    https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html or you can use the below command :
    ```
    aws ssm get-parameter --name /aws/service/eks/optimized-ami/1.27/amazon-linux-2/recommended/image_id --region region-code --query "Parameter.Value" --output text

    ```
    replace **1.27** with the EKS version you are using.

    **KeyName**: An EC2 Key Pair to allow SSH access to the instances.

    **VpcId**: Give the VpcId value obtained from the outputs in step 2.

    **Subnets**: Give the SubnetIds values obtained from the outputs in step 2.

4- Create configmap file to enable worker nodes to join your cluster.

```
vim ~/.kube/aws-auth-cm.yaml
```
paste the configmap file and replace rolearn with node iam role arn.

```
apiVersion: v1
kind: ConfigMap
metadata:
 name: aws-auth
 namespace: kube-system
data:
 mapRoles: |
   - rolearn:  <ARN of instance role>
     username: system:node:{{EC2PrivateDNSName}}
     groups:
       - system:bootstrappers
       - system:nodes
```

```
kubectl apply -f ~/.kube/aws-auth-cm.yaml --kubeconfig ~/.kube/<name of kubeconfig file>
```

5- create docker file to dockerize ping-pong api and push image to dockerhub.
```
docker build  -t samarabdelaziz/ping-pong-api .
docker push samarabdelaziz/ping-pong-api

```

6- create namespace on EKS cluster.
```
kubectl create ns ping-pong-api
```
7- Create helm chart templates to deploy ping-pong api on EKS cluster .
```
helm upgrade -i  ping-pong-api Ping-Pong-API/helm -n ping-pong-api
```

8- ELB will be created on aws , so you can use the dns name with port 3000 to access your api.
