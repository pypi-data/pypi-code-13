"""
Handles extracting information from the POM file.
"""
import untangle


def get_pom_version(pom_file):
    pom = untangle.parse(pom_file)
    return pom.project.version.cdata


def get_pom_name(pom_file):
    pom = untangle.parse(pom_file)
    return pom.project.artifactId.cdata


def get_target_file_name(pom_file):
    pom = untangle.parse(pom_file)
    return '{0}-{1}.zip'.format(pom.project.artifactId.cdata, pom.project.version.cdata)
