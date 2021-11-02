from kfp.v2.dsl import *

@component(
    packages_to_install=["google-cloud-aiplatform"],
    output_component_file="deploy_model.yaml"
)
def deploy_model(
    model: Input[Model],
    project: str,
    region: str,
    vertex_endpoint: Output[Artifact],
    vertex_model: Output[Model]
):
    from google.cloud import aiplatform

    aiplatform.init(project=project, location=region) # 1

    deployed_model = aiplatform.Model.upload( # 2
        display_name="simple-mnist-pipeline",
        artifact_uri = model.uri,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-6:latest"
    )
    endpoint = deployed_model.deploy(machine_type="n1-standard-4") # 3

    # Save data to the output params
    vertex_endpoint.uri = endpoint.resource_name # 4
    vertex_model.uri = deployed_model.resource_name 
