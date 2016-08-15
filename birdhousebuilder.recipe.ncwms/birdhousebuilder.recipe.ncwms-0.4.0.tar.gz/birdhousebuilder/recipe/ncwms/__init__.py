# -*- coding: utf-8 -*-

"""
Recipe ncwms

http://reading-escience-centre.github.io/edal-java/ncWMS_user_guide.html
"""

import os
import pwd
import shutil
import logging
from mako.template import Template

import zc.buildout
import zc.recipe.deployment
from zc.recipe.deployment import Configuration
import birdhousebuilder.recipe.conda
import birdhousebuilder.recipe.tomcat
from birdhousebuilder.recipe.tomcat import make_dirs, unzip

# config_props = Template(filename=os.path.join(os.path.dirname(__file__), "config.properties"))
ncwms_xml = Template(filename=os.path.join(os.path.dirname(__file__), "ncWMS2.xml"))
config_xml = Template(filename=os.path.join(os.path.dirname(__file__), "config.xml"))


def split_args(args):
    if args is None:
        return []
    
    all_args = []
    args = args.strip()
    if args:
        lines = args.split('\n')
        lines = [l.strip() for l in lines]
        for line in lines:
            arg_list = line.split(' ')
            arg_list = [arg.strip().split('=') for arg in arg_list]
            for arg_pair in arg_list:
                all_args.append((arg_pair[0].strip(), arg_pair[1].strip()))
    return all_args


class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs ncWMS2/tomcat with conda and setups the WMS configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.options['name'] = self.options.get('name', self.name)
        self.name = self.options['name']

        self.logger = logging.getLogger(name)

        # tomcat
        self.options['pkgs'] = self.options.get('pkgs', 'ncwms2=2.0.4')
        self.tomcat = birdhousebuilder.recipe.tomcat.Recipe(self.buildout, self.name, self.options)

        # ncwms home with configs
        self.options['ncwms-home'] = self.options['ncwms_home'] = os.path.join(self.options['catalina-base'], 'conf', 'ncWMS2')
            
        # ncwms config options
        self.options['elementLifetimeMinutes'] = self.options.get('elementLifetimeMinutes', '0.0')
        self.options['inMemorySizeMB'] = self.options.get('inMemorySizeMB', '256')
        self.dynamic_services = split_args(self.options.get('dynamic-services'))
        if not self.dynamic_services:
            self.dynamic_services = [
                ('outputs', os.path.join(self.tomcat.prefix, 'var', 'lib', 'pywps', 'outputs')),
                ('cache', os.path.join(self.tomcat.prefix, 'var', 'lib', 'pywps', 'cache')),
                ('uploads', os.path.join(self.tomcat.prefix, 'var', 'lib', 'phoenix', 'uploads'))]
        self.options['contact'] = self.options.get('contact', 'Birdhouse Admin')
        self.options['email'] = self.options.get('email', '')
        self.options['organization'] = self.options.get('organization', 'Birdhouse')
        self.options['title'] = self.options.get('title', 'Birdhouse ncWMS2 Server')
        self.options['abstract'] = self.options.get('abstract', 'ncWMS2 Web Map Service used in Birdhouse')
        self.options['keywords'] = self.options.get('keywords', 'birdhouse,ncwms,wms')
        self.options['url'] = self.options.get('url', 'http://bird-house.github.io/')
        self.options['allowglobalcapabilities'] = self.options.get('allowglobalcapabilities', 'true')
        self.options['enablecache'] = self.options.get('enablecache', 'true')
        self.options['updateInterval'] = self.options.get('updateInterval', '1')

    def install(self, update=False):
        installed = []
        installed += list(self.tomcat.install(update))
        installed += list(self.install_war())
        # installed += list(self.install_config_properties()) # TODO: should be skipped with ncwms 2.2.x
        installed += list(self.install_config_context())
        installed += list(self.install_wms_config())
        return installed

    def install_war(self):
        # make sure ncWMS2.war gets updated and remove app
        app_path =  os.path.join(self.tomcat.options['catalina-base'], 'webapps', 'ncWMS2')
        if os.path.exists(app_path):
            shutil.rmtree(app_path)
        # copy war file
        # TODO: does not work with < 2.2.x
        war_file = os.path.join(self.tomcat.options['catalina-base'], 'webapps', 'ncWMS2.war')
        shutil.copy(
            os.path.join(self.tomcat.options['catalina-home'], 'webapps', 'ncWMS2.war'),
            war_file)
        # make sure it is unpacked
        # TODO: skip this with ncwms 2.2.x
        #unzip(
        #    self.tomcat.options['catalina-base'],
        #    os.path.join(self.tomcat.options['catalina-home'], 'webapps', 'ncWMS2.war'))
        return tuple()

    ## def install_config_properties(self):
    ##     """
    ##     used until ncWMS2 2.1.x
    ##     """
    ##     text = config_props.render(**self.options)
    ##     config = Configuration(self.buildout, 'config.properties', {
    ##         'deployment': self.tomcat.deployment_name,
    ##         'directory': os.path.join(self.options['catalina-base'], 'webapps', 'ncWMS2', 'WEB-INF', 'classes' ),
    ##         'text': text})
    ##     return [config.install()]

    def install_config_context(self):
        """
        used since ncWMS2 2.2.0
        """
        text = ncwms_xml.render(**self.options)
        config = Configuration(self.buildout, 'ncWMS2.xml', {
            'deployment': self.tomcat.deployment_name,
            'directory': os.path.join(self.options['catalina-base'], 'conf', 'Catalina', 'localhost' ),
            'text': text})
        return [config.install()]

    def install_wms_config(self):
        text = config_xml.render(dynamic_services=self.dynamic_services, **self.options)
        make_dirs(self.options['ncwms-home'], self.options['user'], mode=0o755)
        config = Configuration(self.buildout, 'config.xml', {
            'deployment': self.tomcat.deployment_name,
            'directory': self.options['ncwms-home'],
            'text': text})
        return [config.install()]

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

