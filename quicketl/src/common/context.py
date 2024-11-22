import boto3

class QuickContext:


    def __init__(self):

        self.s3_client = boto3.client("s3")
        self.glue_client = boto3.client("glue")
        self.sqs_client = boto3.client("sqs")
        self.sns_client = boto3.client("sns")


        self.s3_resource = boto3.client("s3")
