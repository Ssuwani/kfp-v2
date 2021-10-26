import kfp
import kfp.dsl as dsl
from kfp.v2.dsl import component
from kfp import compiler


@component
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b


@dsl.pipeline(
    name='addition-pipeline',
    description='An example pipeline that performs addition calculations.',
    # pipeline_root='gs://my-pipeline-root/example-pipeline'
)
def add_pipeline(a: float = 1, b: float = 7):
    add_task = add(a, b)


if __name__ == '__main__':
    compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=add_pipeline, package_path='pipeline.yaml')
