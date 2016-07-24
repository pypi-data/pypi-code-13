import click
import json

import hark_builder.build
import hark_builder.imagecache
import hark_builder.context
import hark_builder.runner

from hark_builder.exceptions import BuildFailed, UploadFailed

import hark.log
from hark.cli.util import loadLocalContext


@click.group(name='hark_builder')
@click.pass_context
@click.option('--hark-home', envvar='HARKHOME', type=str)
@click.option('--log-level', envvar='LOGLEVEL', type=str, default='INFO')
def main(ctx, hark_home, log_level):
    hark.log.setLevel(log_level)
    harkctx = loadLocalContext(
        hark_home, context_class=hark_builder.context.BuilderContext)

    hark.log.setOutputFile(harkctx.log_file())

    ctx.obj = harkctx

    pass


@main.command(name='list')
def list_builds():
    """List available machine build scripts"""
    builds = hark_builder.build.Build.all()

    click.secho('Found %d builds' % len(builds), fg='green')
    for b in builds:
        click.echo(b.name)


@main.command(name='run')
@click.pass_obj
@click.option(
    '--name', prompt='Which build', required=True)
@click.option(
    '--version',
    prompt='What version of the image', type=int, required=True)
@click.option(
    '--override-local', is_flag=True, default=False,
    help='Run the build even if the artifact already exists locally'
)
@click.option(
    '--confirm-upload', is_flag=True, default=False,
    help='Prompt for confirmation before uploading')
@click.option(
    '--aws-access-key-id',
    envvar='AWS_ACCESS_KEY_ID', type=str, default=None)
@click.option(
    '--aws-secret-access-key',
    envvar='AWS_SECRET_ACCESS_KEY', type=str, default=None)
def run_build(
        ctx, name, version,
        override_local, confirm_upload,
        aws_access_key_id, aws_secret_access_key):
    """Run a machine build"""
    build = hark_builder.build.Build.by_name(name)

    image_cache = hark_builder.imagecache.S3ImageCache(
        aws_access_key_id, aws_secret_access_key)

    runner = hark_builder.runner.BuildRunner(
        build, image_cache, ctx.builder_path, version)

    click.secho('Running packer build: %s' % build, fg='green')

    exists = runner.build_artifact_exists()

    if exists and not override_local:
        stats = runner.build_artifact_info()
        click.secho('Build artifact already exists locally:', fg='red')
        click.echo(json.dumps(stats, indent=4))
        click.secho('Run with --override-local to build anyway.')
        raise click.Abort

    try:
        hark.log.debug('running image build: %s', build)
        runner.run_build(force=exists)
    except BuildFailed as e:
        click.secho('Build failed: %s' % e, fg='red')
        raise click.Abort
    else:
        click.secho('Build succeeded.', fg='green')

    click.secho('Uploading build artifact to remote image cache', fg='green')

    stats = runner.build_artifact_info()
    click.secho('Build artifact:', fg='green')
    click.echo(json.dumps(stats, indent=4))

    if confirm_upload and not click.confirm('Ready to upload now?'):
        raise click.Abort

    click.secho('Uploading to %s' % runner.target_image.s3_path(), fg='blue')

    try:
        hark.log.debug('uploading artifact from image build: %s', build)
        length = runner.build_artifact_size()
        msg = 'Uploading:'
        with click.progressbar(length=length, label=msg) as bar:
            def cb(count):
                bar.update(count)
            runner.upload_build_artifact(callback=cb)
    except UploadFailed as e:
        click.secho('Upload failed: %s' % e, fg='red')
        raise click.Aborted
    else:
        click.secho('Upload succeeded.', fg='green')
