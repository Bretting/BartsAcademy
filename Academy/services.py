import boto3
import os

class DigitalOceanSpacesService:
    def __init__(self, access_key, secret_key, region_name='ams3', endpoint_url='https://ams3.digitaloceanspaces.com'):
        self.client = boto3.client(
            's3',
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def initiate_multipart_upload(self, bucket_name, object_name):
        response = self.client.create_multipart_upload(Bucket=bucket_name, Key=object_name)
        return response['UploadId']

    def copy_part(self, bucket_name, upload_id, object_name, part_number, copy_source):
        response = self.client.upload_part_copy(
            Bucket=bucket_name,
            Key=object_name,
            UploadId=upload_id,
            PartNumber=part_number,
            CopySource=copy_source
        )
        return {
            'ETag': response['CopyPartResult']['ETag'],
            'PartNumber': part_number
        }

    def complete_multipart_upload(self, bucket_name, object_name, upload_id, parts):
        response = self.client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=object_name,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        return response

    def reassemble_chunks_remotely(self, bucket_name, chunks_prefix, final_filename):
        # Step 1: Initiate multipart upload
        upload_id = self.initiate_multipart_upload(bucket_name, final_filename)

        # Step 2: List chunks
        result = self.client.list_objects_v2(Bucket=bucket_name, Prefix=chunks_prefix)
        chunks = [obj['Key'] for obj in result['Contents']]
        chunks.sort()  # Ensure chunks are in the correct order

        # Step 3: Copy chunks as parts
        parts = []
        for i, chunk in enumerate(chunks):
            part_number = i + 1
            copy_source = f'{bucket_name}/{chunk}'
            part = self.copy_part(bucket_name, upload_id, final_filename, part_number, copy_source)
            parts.append(part)

        # Step 4: Complete multipart upload
        self.complete_multipart_upload(bucket_name, final_filename, upload_id, parts)

        # Return the URL of the reassembled file
        return f'https://{bucket_name}.ams3.digitaloceanspaces.com/media/videos{final_filename}'
