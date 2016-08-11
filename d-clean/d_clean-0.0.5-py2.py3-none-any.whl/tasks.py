from d_clean import common


def clean_all(dry_run=False):
    clean_stopped_containers(dry_run=dry_run)
    clean_images_not_in_use(dry_run=dry_run)
    clean_dangling_images(dry_run=dry_run)


def clean_dangling_images(dry_run=False):
    danglingImages = common.shell_call('docker images -f "dangling=true" -q')

    if danglingImages:
        images = danglingImages.replace('\n', ' ')
        if dry_run:
            print('will remove danglingImages {}'.format(images))
        else:
            print('removing dangling images {}'.format(images))
            common.shell_call('docker rmi $(docker images -f "dangling=true" -q)')
    else:
        print('no danglingImages images to remove')


def clean_stopped_containers(dry_run=False):
    stoppedContainers = common.shell_call('docker ps -a -q -f status=exited')

    if stoppedContainers:
        conainers = stoppedContainers.replace('\n', ' ')
        if dry_run:
            print('will remove stoppedContainers {}'.format(conainers))
        else:
            print('removing stopped containers {}'.format(conainers))
            common.shell_call('docker rm -v $(docker ps -a -q -f status=exited)')
    else:
        print('no stoppedContainers to remove')


def clean_images_not_in_use(dry_run=False):
    imagesNotInUse = common.shell_call('docker images -a -q')

    if imagesNotInUse:
        conainers = imagesNotInUse.replace('\n', ' ')
        if dry_run:
            print('will remove imagesNotInUse {}'.format(conainers))
        else:
            print('removing images not in use {}'.format(conainers))
            common.shell_call('docker rmi $(docker images -a -q)')
    else:
        print('no imagesNotInUse to remove')
