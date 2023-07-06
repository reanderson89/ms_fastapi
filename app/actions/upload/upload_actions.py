import io
import csv
import logging
from os import getenv
from time import time
import boto3
from datadog.api.exceptions import ClientError
from app.actions.base_actions import BaseActions
from app.actions.clients.user import ClientUserActions
from app.exceptions import ExceptionHandling


aws_access_key_id = getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
aws_bucket_name = getenv("AWS_BUCKET_NAME")
role_arn = getenv("AWS_ROLE_ARN")


class UploadActions(BaseActions):

	@classmethod
	async def get_s3_client(cls):
		session = boto3.Session(
			aws_access_key_id=aws_access_key_id,
			aws_secret_access_key=aws_secret_access_key
		)
		client = session.client('sts')
		response = client.assume_role(RoleArn=role_arn, RoleSessionName="UploadPresignedUrl")

		session = boto3.Session(
			aws_access_key_id=response['Credentials']['AccessKeyId'],
			aws_secret_access_key=response['Credentials']['SecretAccessKey'],
			aws_session_token=response['Credentials']['SessionToken']
		)
		client = session.client('sts')
		s3_client = session.client('s3')

		return s3_client

	@classmethod
	async def generate_upload_url(cls, upload_type, file_name, client_uuid=None):
		fname = file_name
		if upload_type == "roster" and client_uuid:
			file_type = fname.split(".")[-1]
			if file_type != "csv":
				await ExceptionHandling.custom415("File type must be csv")

			fname = f"{client_uuid}/uploads/{fname}"

		if upload_type == "image" and client_uuid:
			fname = f"{client_uuid}/images/{fname}"

		s3_response = await cls.create_presigned_post(aws_bucket_name, fname)

		return s3_response

	@classmethod
	async def create_presigned_post(cls, bucket_name, object_name, fields=None, conditions=None, expiration=100):
		"""Generate a presigned URL S3 POST request to upload a file

		:param bucket_name: string
		:param object_name: string
		:param fields: Dictionary of prefilled form fields
		:param conditions: List of conditions to include in the policy
		:param expiration: Time in seconds for the presigned URL to remain valid
		:return: Dictionary with the following keys:
			url: URL to post to
			fields: Dictionary of form fields and values to submit with the POST
		:return: None if error.
		"""

		s3_client = await cls.get_s3_client()

		try:
			response = s3_client.generate_presigned_post(
				bucket_name,
				object_name,
				Fields=fields,
				Conditions=conditions,
				ExpiresIn=expiration
			)
		except ClientError as e:
			logging.error(e)
			return None

		return response


	@classmethod
	async def process_csv_file(cls, s3_file_name, client_uuid):
		s3_client = await cls.get_s3_client()

		try:
			response = s3_client.get_object(
				Bucket=aws_bucket_name,
				Key=s3_file_name.file_name
			)
		except ClientError as e:
			logging.error(e)
			return None

		with io.StringIO(response['Body'].read().decode('utf-8')) as stream:
			csv_reader = csv.DictReader(stream, delimiter=',')
			csv_list = [row for row in csv_reader]

		processed_users = [await ClientUserActions.create_client_user(user, {"client_uuid": client_uuid}) for user in csv_list]

		return processed_users
