#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform

def run():
	from onyx.core import core
	core.run('0.0.0.0', port=8080 , debug=True)

def install():
	if platform.system() == "Linux":
		#os.system("sh blabla")
		from migrate.versioning import api
		from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
		from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
		from onyx.core import db
		import os.path
		db.create_all()
		if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
		    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		else:
		    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
		                        api.version(SQLALCHEMY_MIGRATE_REPO))
	else:
		from migrate.versioning import api
		from onyx.bddconfig import SQLALCHEMY_DATABASE_URI
		from onyx.bddconfig import SQLALCHEMY_MIGRATE_REPO
		from onyx.core import db
		import os.path
		db.create_all()
		if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
		    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		else:
		    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
		                        api.version(SQLALCHEMY_MIGRATE_REPO))

def maj():
	if platform.system() == "Linux":
		os.system("sh blabla")
		import imp
		from migrate.versioning import api
		from onyx.core import db
		from bddconfig import SQLALCHEMY_DATABASE_URI
		from bddconfig import SQLALCHEMY_MIGRATE_REPO
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
		                                          SQLALCHEMY_MIGRATE_REPO,
		                                          tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))
	else:
		import imp
		from migrate.versioning import api
		from onyx.core import db
		from bddconfig import SQLALCHEMY_DATABASE_URI
		from bddconfig import SQLALCHEMY_MIGRATE_REPO
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
		                                          SQLALCHEMY_MIGRATE_REPO,
		                                          tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))


