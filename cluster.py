def GenerateConfig(context):
    cluster_name = context.properties['CLUSTER_NAME']
    cluster_zone = context.properties['CLUSTER_ZONE']
    nodepool_name = context.properties['POOL_NAME']
    num_nodes = context.properties['NUM_NODES']

    resources = []
    outputs = []

    resources.append({
        'name': cluster_name,
        'type': 'container.v1.cluster',
        'properties': {
            'zone': cluster_zone,
            'cluster': {
                'name': cluster_name,
                'nodePools': [
                    {
                        'name': nodepool_name,
                        'initialNodeCount': num_nodes,
                        'config':{
                            'machineType': 'n1-standard-2',
                            'oauth_scopes': [
                                'https://www.googleapis.com/auth/' + scopes 
                                for scopes in [
                                    'compute',
                                    'cloud-platform',
                                    'logging.write',
                                    'monitoring',
                                    'service.management.readonly',
                                    'servicecontrol',
                                    'devstorage.read_write'
                                ]
                            ],
                            'diskType': 'pd-ssd' 
                        },
                        'autoscaling': {
                            'enabled': True,
                            'minNodeCount': 4,
                            'maxNodeCount': 6
                        }
                    }
                ]
            }
        }
    })
    if context.properties['gke-nodepool']:
        resources.append({
            'name': nodepool_name,
            'type': 'container.v1.nodePool',
            'properties': {
                'zone': cluster_zone,
                'clusterId': '$(ref.' + cluster_name + '.name)',
                'nodePool': {
                    'name': nodepool_name,
                    'initialNodeCount': num_nodes,
                    'config':{
                        'machineType': 'n1-standard-2',
                        'oauth_scopes': [
                            'https://www.googleapis.com/auth/' + scopes 
                            for scopes in [
                                'compute',
                                'cloud-platform',
                                'logging.write',
                                'monitoring',
                                'service.management.readonly',
                                'servicecontrol',
                                'devstorage.read_write'
                            ]
                        ],
                        'diskType': 'pd-ssd' 
                    },
                    'autoscaling': {
                        'enabled': True,
                        'minNodeCount': 4,
                        'maxNodeCount': 6
                    }
                }
            }
        })

    outputs.append({
        'name': 'endpoint',
        'value': '$(ref.' + cluster_name + '.endpoint)'
    })

    return {'resources': resources, 'outputs': outputs}