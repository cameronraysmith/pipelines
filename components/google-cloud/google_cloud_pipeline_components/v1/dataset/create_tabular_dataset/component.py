# Copyright 2023 The Kubeflow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Optional

from google_cloud_pipeline_components.types.artifact_types import VertexDataset
from kfp import dsl
from kfp.dsl import Output


@dsl.container_component
def tabular_dataset_create(
    project: str,
    display_name: str,
    dataset: Output[VertexDataset],
    location: Optional[str] = 'us-central1',
    gcs_source: Optional[str] = None,
    bq_source: Optional[str] = None,
    labels: Optional[dict] = {},
    encryption_spec_key_name: Optional[str] = None,
):
  # fmt: off
  """Creates a new tabular dataset.

  Args:
      display_name: The user-defined name of the Dataset.
          The name can be up to 128 characters long and can be consist
          of any UTF-8 characters.
      gcs_source:
          Google Cloud Storage URI(-s) to the
          input file(s). May contain wildcards. For more
          information on wildcards, see
          https://cloud.google.com/storage/docs/gsutil/addlhelp/WildcardNames.
          examples:
              str: "gs://bucket/file.csv"
              Sequence[str]: ["gs://bucket/file1.csv", "gs://bucket/file2.csv"]
      bq_source: BigQuery URI to the input table.
          example:
              "bq://project.dataset.table_name"
      project: project to retrieve dataset from.
      location: Optional location to retrieve dataset from.
      labels: Labels with user-defined metadata to organize your Tensorboards.
          Label keys and values can be no longer than 64 characters
          (Unicode codepoints), can only contain lowercase letters, numeric
          characters, underscores and dashes. International characters are allowed.
          No more than 64 user labels can be associated with one Tensorboard
          (System labels are excluded).
          See https://goo.gl/xmQnxf for more information and examples of labels.
          System reserved label keys are prefixed with "aiplatform.googleapis.com/"
          and are immutable.
      encryption_spec_key_name: The Cloud KMS resource identifier of the customer
          managed encryption key used to protect the dataset. Has the
          form:
          ``projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key``.
          The key needs to be in the same region as where the compute
          resource is created.
          If set, this Dataset and all sub-resources of this Dataset will be secured by this key.
          Overrides encryption_spec_key_name set in aiplatform.init.
  Returns:
      tabular_dataset: Instantiated representation of the managed tabular dataset resource.
  """
  # fmt: on

  return dsl.ContainerSpec(
      image='gcr.io/ml-pipeline/google-cloud-pipeline-components:2.0.0b3',
      command=[
          'python3',
          '-m',
          'google_cloud_pipeline_components.container.v1.aiplatform.remote_runner',
          '--cls_name',
          'TabularDataset',
          '--method_name',
          'create',
      ],
      args=[
          '--method.project',
          project,
          '--method.location',
          location,
          '--method.display_name',
          display_name,
          dsl.IfPresentPlaceholder(
              input_name='gcs_source', then=['--method.gcs_source', gcs_source]
          ),
          dsl.IfPresentPlaceholder(
              input_name='bq_source', then=['--method.bq_source', bq_source]
          ),
          '--method.labels',
          labels,
          dsl.IfPresentPlaceholder(
              input_name='encryption_spec_key_name',
              then=[
                  '--method.encryption_spec_key_name',
                  encryption_spec_key_name,
              ],
          ),
          '--executor_input',
          '{{$}}',
          '--resource_name_output_artifact_uri',
          dataset.uri,
      ],
  )
