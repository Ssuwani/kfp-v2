import kfp
from kfp.v2 import dsl
from kfp import components

PROJECT_ID = "abstract-flame-330901"
REGION = "us-central1"

@dsl.pipeline(
    name="mnist-pipeline",
    description="mnist pipeline tutorial",
    pipeline_root="gs://suwan"
)
def pipeline(
    project: str = PROJECT_ID,
    region: str = REGION
):
    load_data = components.load_component_from_file("load_data.yaml")
    train_linear = components.load_component_from_file("train_linear.yaml")
    train_cnn = components.load_component_from_file("train_cnn.yaml")
    evaluate_models = components.load_component_from_file("evaluate_models.yaml")
    deploy_model = components.load_component_from_file("deploy_model.yaml")
    load_data_task = load_data()
    train_linear_task = train_linear(
        dataset=load_data_task.outputs["dataset"]
    )
    train_cnn_task = train_cnn(
        dataset=load_data_task.outputs["dataset"]
    )
    evaluate_models_task = evaluate_models(
        dataset=load_data_task.outputs["dataset"],
        model_linear=train_linear_task.outputs["output_model"],
        model_cnn=train_cnn_task.outputs["output_model"]
    )
    deploy_task = deploy_model(
        model=evaluate_models_task.outputs["model_best"],
        project=project,
        region=region
    )

client = kfp.Client("https://22767e8e71dc72a3-dot-us-central1.pipelines.googleusercontent.com/")

client.create_run_from_pipeline_func(
    pipeline,
    arguments={},
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
)    
