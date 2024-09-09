from google.cloud import storage


class GcpStorage:
    def uploadFile(self, bucket_name, src, dest) -> str:
        storage_client = storage.Client.from_service_account_json("gcp-testing-431723-3a29a9bb2d25.json")
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(dest)

        with open(src, "rb") as file:
            blob.upload_from_file(file)
            
        return
