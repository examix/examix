import os, json
from typing import Optional, Sequence

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

def process_document(fp) -> dict:
    project_id = 'potent-poetry-411704'
    #os.getenv("GCLOUD_PROJECT_ID")
    location = "us" # Format is "us" or "eu"
    processor_id = '3527739efa1575b3'
        #os.getenv("GCLOUD_PROCESSOR_ID"))
    processor_version = "rc" # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
    mime_type = "application/pdf" # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types

    assert project_id
    assert processor_id

    doc = __process_document(project_id, location, processor_id, processor_version, fp, mime_type)
    return json.loads(documentai.Document.to_json(doc))

def __process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    fp: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    image_content = fp.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document

