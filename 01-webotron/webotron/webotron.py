import boto3
import click

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "webotron deploys websites to aws"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    "List all objects in s3 buckets"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)
    pass

if __name__ == '__main__':
    cli()