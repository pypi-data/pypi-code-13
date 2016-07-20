import os
import sh
import re
from copy import copy
from flask import jsonify, current_app, abort, request
from flask.views import MethodView


class BrowseApi(MethodView):
    methods = [ 'GET' ]

    def get(self, repo_name, obj_path):

        # Add HEAD: to path by default
        if not re.match('.*\:.*', obj_path):
            obj_path = 'HEAD:{}'.format(obj_path)

        # Assume normal directory
        repo_dir = os.path.join(current_app.config['REPO_DIR'], repo_name)

        # Look for bare repository
        if not os.path.isdir(repo_dir):
            repo_dir = '{}.git'.format(repo_dir)
        
        # 404 if repository can't be found
        if not os.path.isdir(repo_dir):
            abort(404)

        # Set current directory to bare repo
        git = sh.git.bake(_cwd=repo_dir)

        # Get object type
        try:
            obj_type = str(git('cat-file', '-t', obj_path)).rstrip()
        except sh.ErrorReturnCode_128 as e:
            if "Not a valid object name" in e.stderr:
                abort(404)
            raise e

        # Recursive tree walk function
        def traverse_tree(tree_path, depth):
            obj_content = []

            for obj in git('cat-file', '-p', tree_path, _iter=True):

                obj_data = obj.split()
                obj_dict = {
                    'permissions': obj_data[0],
                    'type': obj_data[1],
                    'treeish': obj_data[2],
                    'name': obj_data[3]
                }

                if obj_dict['type'] == 'tree' and depth:
                    if re.match('.*\:$', tree_path):
                        sub_tree_path = tree_path + obj_dict['name']
                    else:
                        sub_tree_path = tree_path + '/' + obj_dict['name']
                    obj_dict['content'] = traverse_tree(sub_tree_path, depth-1)

                obj_content.append(obj_dict)

            return obj_content

        # Tree contains multiple objects, so scan (default 3 depth)
        if obj_type == "tree":
            traverse_depth = int(request.args.get('depth', 3))
            obj_content = traverse_tree(obj_path, traverse_depth)

        # Print blob content directly
        elif obj_type == "blob":
            obj_content = str(git('cat-file', '-p', obj_path))

        # Cannot browse other object types
        else:
            abort(404)

        return jsonify({ 'type': obj_type, 'content': obj_content })
