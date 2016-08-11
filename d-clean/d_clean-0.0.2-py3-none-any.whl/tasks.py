from fabric.api import task, local, execute, hide
from fabric.context_managers import settings


@task
def clean_all(dry_run=False):
    execute(clean_stopped_containers, dry_run=dry_run)
    execute(clean_images_not_in_use, dry_run=dry_run)
    execute(clean_dangling_images, dry_run=dry_run)


@task
def clean_dangling_images(dry_run=False):
    with hide('output', 'running'), settings(warn_only=True):
        danglingImages = local('docker images -f "dangling=true" -q', capture=True)

        if danglingImages:
            images = danglingImages.replace('\n', ' ')
            if dry_run:
                print('will remove danglingImages {}'.format(images))
            else:
                print('removing dangling images {}'.format(images))
                local('docker rmi $(docker images -f "dangling=true" -q)')
        else:
            print('no danglingImages images to remove')


@task
def clean_stopped_containers(dry_run=False):
    with hide('output', 'running'), settings(warn_only=True):
        stoppedContainers = local('docker ps -a -q -f status=exited', capture=True)

        if stoppedContainers:
            conainers = stoppedContainers.replace('\n', ' ')
            if dry_run:
                print('will remove stoppedContainers {}'.format(conainers))
            else:
                print('removing stopped containers {}'.format(conainers))
                local('docker rm -v $(docker ps -a -q -f status=exited)')
        else:
            print('no stoppedContainers to remove')


@task
def clean_images_not_in_use(dry_run=False):
    with hide('output', 'running'), settings(warn_only=True):
        imagesNotInUse = local('docker images -a -q', capture=True)

        if imagesNotInUse:
            conainers = imagesNotInUse.replace('\n', ' ')
            if dry_run:
                print('will remove imagesNotInUse {}'.format(conainers))
            else:
                print('removing images not in use {}'.format(conainers))
                local('docker rmi $(docker images -a -q)')
        else:
            print('no imagesNotInUse to remove')
