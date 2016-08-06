# -*- coding: utf-8 -*-
from sphinx.domains import Domain, ObjType
from sphinx.util.nodes import make_refnode


class ReSTMarkup(object):
    """
    Description of generic reST markup.
    """

    def add_target_and_index(self, name, sig, signode):
        targetname = self.objtype + '-' + name
        if targetname not in self.state.document.ids:
            signode['names'].append(targetname)
            signode['ids'].append(targetname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)

            objects = self.env.domaindata['rst']['objects']
            key = (self.objtype, name)
            if key in objects:
                self.state_machine.reporter.warning(
                    'duplicate description of %s %s, ' % (self.objtype, name) +
                    'other instance in ' + self.env.doc2path(objects[key]),
                    line=self.lineno)
            objects[key] = self.env.docname
        indextext = self.get_index_text(self.objtype, name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              targetname, '', None))

    def get_index_text(self, objectname, name):
        if self.objtype == 'directive':
            return '%s (directive)' % name
        elif self.objtype == 'role':
            return '%s (role)' % name
        return ''


class WebAPIDomain(Domain):
    """WebAPI domain."""
    name = 'webapi'
    label = 'Web API'

    object_types = {
        'type': ObjType('type', 'type'),
    }
    directives = {}
    roles = {}
    initial_data = {
        'objects': {},  # objtype, fullname -> docname
    }

    def clear_doc(self, docname):
        for (typ, name), doc in list(self.data['objects'].items()):
            if doc == docname:
                del self.data['objects'][typ, name]

    def merge_domaindata(self, docnames, otherdata):
        # XXX check duplicates
        for (typ, name), doc in otherdata['objects'].items():
            if doc in docnames:
                self.data['objects'][typ, name] = doc

    def add_object(self, objtype, fullname, docname):
        self.data[objtype, fullname] = docname

    def add_type(self, fullname, docname):
        self.add_object('type', fullname, docname)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        objects = self.data['objects']
        objtypes = self.objtypes_for_role(typ)
        for objtype in objtypes:
            if (objtype, target) in objects:
                return make_refnode(builder, fromdocname,
                                    objects[objtype, target],
                                    objtype + '-' + target,
                                    contnode, target + ' ' + objtype)

    def resolve_any_xref(self, env, fromdocname, builder, target,
                         node, contnode):
        objects = self.data['objects']
        results = []
        for objtype in self.object_types:
            if (objtype, target) in self.data['objects']:
                results.append(('webapi:' + self.role_for_objtype(objtype),
                                make_refnode(builder, fromdocname,
                                             objects[objtype, target],
                                             objtype + '-' + target,
                                             contnode, target + ' ' + objtype)))
        return results

    def get_objects(self):
        for (typ, name), docname in self.data['objects'].items():
            yield name, name, typ, docname, typ + '-' + name, 1
