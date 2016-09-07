#!/usr/bin/env python
import os
import sys
from subprocess import Popen

import github3
from git import Repo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from classwerk.utils import *


def add_subparser(subparser):
    parser = subparser.add_parser("create-repos", help='manage student groups')
    parser.add_argument('-f', '--force', action='store_const', const=True, help='force push even if repo exists',
                            required=False, default=False)
    parser.add_argument('-F', '--filter', nargs='*', dest='filter', help='filter by team name', default=None)
    parser.set_defaults(command=create_repo)

def get_travis_badge(driver, page):
    driver.get(page)
    img = driver.find_element(By.ID, 'status-image-popup').find_element_by_tag_name('img')
    travis_badge = img.get_attribute('src')
    return travis_badge

def create_repo(args, gh_handle, **kwargs):

    c = get_config(args.config)
    org = gh_handle.organization(c['organization'])
    all_teams = org.teams()

    print os.path.join(os.getcwd(), "id_rsa")
    print "=" * 80
    print "Creating repositories for %s from %s" % (c['organization'], c['source'])
    print "=" * 80

    if c['enable_travis']:
        driver = webdriver.Firefox()
        driver.get(c['travis_host'])
        driver.implicitly_wait(60)
        print "Waiting 60 seconds for Travis authentication..."
        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "navigation-anchor signed-in")]')))
        except TimeoutException:
            print "Loading TravisCI took too much time!"
            sys.exit(1)

    teams = filter_teams(c['teams'], args.filter)

    for team in teams:
        members = c['teams'][team]
        name = "%s-%s" % (c['prefix'], team)
        repo_path = "git@github.com:%s/%s.git" % (c['organization'], name)
        repo_short = "%s/%s" % (c['organization'], name)

        print "-> %s" % name

        # Create repo and add team to collaborators
        try:
            org.create_repository(name, private=c['private'])
            print "  \-> %s" % Colors.success("Created repo")
        except github3.exceptions.UnprocessableEntity:
            # Already exists
            print "  \-> %s" % Colors.warn("Repo already exists")

        # Enable travis for repo
        if c['enable_travis']:
            FNULL = open(os.devnull, 'w')
            p = Popen(["travis", "enable", "-r", repo_short], stdout=FNULL)
            p_output = p.communicate()[0]
            if p.returncode != 0:
                print "  \-> %s" % Colors.error("Error enabling TravisCI [%s]" % p_output)
            else:
                print "  \-> %s" % Colors.success("Enabled TravisCI")


            p = Popen(["travis", "sshkey", "--upload", os.path.join(os.getcwd(), "id_rsa"), "-r", repo_short], stdout=FNULL)
            p_output = p.communicate()[0]
            if p.returncode != 0:
                print "  \-> %s" % Colors.error("Error adding SSH key to TravisCI [%s]" % p_output)
            else:
                print "  \-> %s" % Colors.success("Added SSH key for TravisCI")

            travis_url = '%s/%s' % (c['travis_host'], repo_short)
            badge_url = get_travis_badge(driver, travis_url)
            travis_badge = '[![Build Status](%s)](%s)' % (badge_url, travis_url)
            print "  \-> %s" % ("Found badge [%s]" % badge_url)

        else:
            travis_badge = ''
            travis_url = ''

        with TemporaryDirectory() as temp_dir:
            # Initializes repo and adds README
            repo = Repo.init(temp_dir)
            readme_path = os.path.join(temp_dir, "README.md")


            with open(readme_path, 'wb') as f:
                f.write(c['readme'].format(travis_badge=travis_badge, travis_url=travis_url))

            repo.index.add([readme_path])                        # add it to the index
            # Commit the changes to deviate masters history
            repo.index.commit("Initial commit.")

            origin = repo.create_remote('origin', repo_path)

            # Add upstream branch that tracks source repo
            upstream = repo.create_remote('upstream', c['source'])
            upstream.fetch()

            repo.git.checkout('upstream/%s' % c['source-branch'], track=True, b='upstream')
            repo.heads.upstream.checkout()

            repo.heads.master.checkout()
            repo.git.merge('upstream')


            # Push everything to Github
            print "  \-> Pushing starter code"
            for status in repo.remotes.origin.push(all=True, force=args.force):
                message = "Pushing [%s] resulted in: %s" % (status.local_ref.name, status.summary)

                if status.flags > 1024: # ERROR
                    print "    \-> %s" % Colors.error(message)
                else:
                    print "    \-> %s" % Colors.success(message)


        # Add team and course staff as collaborators
        for team in all_teams:
            if team.name in [name, 'Owners']:
                team.add_repository(repo_short)
                team.edit(team.name, permission='push')
                print "  \-> %s" % Colors.success("Added team [%s] as collaborators" % team.name)



