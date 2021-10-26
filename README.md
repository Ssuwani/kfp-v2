# kfp-v2

Follow up https://www.kubeflow.org/docs/components/pipelines/sdk/v2

#### Install 

```bash
pip install kfp --upgrade
```



### Add Task

Calculates sum of two arguments

**Inputs**

| Name | Type  | Default | Description   |
| ---- | ----- | ------- | ------------- |
| a    | float | 1       | first number  |
| b    | float | 7       | second number |

**Output**

| Name | Type  | Default | Description          |
| ---- | ----- | ------- | -------------------- |
|      | float | 8       | sum of two arguments |

<img src="add_pipeline/images/demo.png" width="500"/>

**Usage:**

```bash
python add_pipeline/pipeline.py
```



### Build Components

package as a Docker container image



