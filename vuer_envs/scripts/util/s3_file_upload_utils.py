import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def upload_files_to_s3(file_list, bucket_name, s3_folder=None):
    """
    Upload a list of files to an S3 bucket and make them public.

    :param file_list: List of file paths to upload
    :param bucket_name: Name of the S3 bucket
    :param s3_folder: (Optional) Folder path in the S3 bucket where files should be uploaded
    """
    # Initialize S3 client
    s3_client = boto3.client("s3")

    uploaded_files_urls = []

    for file_path in file_list:
        try:
            # Extract file name from file path
            file_name = file_path.split("/")[-1]

            # If a folder path is provided, include it in the S3 object key
            s3_key = f"{s3_folder}/{file_name}" if s3_folder else file_name

            # Upload the file to the S3 bucket
            s3_client.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs={"ACL": "public-read"},  # Make the file publicly accessible
            )

            # Construct the public URL of the uploaded file
            file_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
            uploaded_files_urls.append(file_url)

            print(f"File '{file_path}' uploaded successfully to {file_url}.")

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except NoCredentialsError:
            print("Error: No AWS credentials found.")
        except PartialCredentialsError:
            print("Error: AWS credentials are incomplete.")
        except Exception as e:
            print(f"An error occurred while uploading '{file_path}': {e}")

    return uploaded_files_urls


if __name__ == "__main__":
    from glob import glob

    # Example usage
    file_list = glob("./*.*")
    bucket_name = "vuer-hub-production"  # Replace with your bucket name

    # Optional: folder name in the bucket where files will be stored
    s3_folder = "assets/lucid-xr"

    uploaded_urls = upload_files_to_s3(file_list, bucket_name, s3_folder)

    print("\nUploaded Files URLs:")
    for url in uploaded_urls:
        print(url, end="\r")
