#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Webotron: Deploy websites with AWS.

Webotron automates the process of deploying static websites to AWS
- Configure AWS s3 list_buckets
    - create list_buckets
    - set them up for static website hosting
    - deploy local files to them
- Configure DNS with AWS Route 53
- Configure a CDN and SSL with AWS CloudFront
"""
import boto3
import click

from bucket import BucketManager

session = None
bucket_manager = None


@click.group()
@click.option('--profile', default=None,
    help="Use a given AWS profile")
def cli(profile):
    """Webotron deploys websites to aws."""
    global session, bucket_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    """List all objects in s3 buckets."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure s3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
