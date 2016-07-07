# -*- coding: utf-8 -*-

from interfaces import ITaxonomy

from zope.component import queryMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.security.interfaces import IPermission
from zope.component.hooks import getSite

from plone import api


_pmf = MessageFactory('plone')


class TaxonomyVocabulary(object):
    # Vocabulary for generating a list of existing taxonomies

    implements(IVocabularyFactory)

    def __call__(self, adapter):
        results = []
        sm = getSite().getSiteManager()
        utilities = sm.getUtilitiesFor(ITaxonomy)

        for (utility_name, utility) in utilities:
            utility_name = utility.name
            utility_title = utility.title

            results.append(SimpleTerm(value=utility_name,
                                      title=utility_title)
                           )

        return SimpleVocabulary(results)


class Vocabulary(object):
    """Vocabulary, generated by the ITaxonomy utility"""

    implements(IVocabulary)

    def __init__(self, name, data, inv_data):
        self.data = data
        self.inv_data = inv_data
        self.message = MessageFactory(name)

    def __iter__(self):
        for term in self.getTerms():
            yield term

    def __len__(self):
        return len(self.getTerms())

    def __contains__(self, identifier):
        return self.getTerm(identifier) is not None

    def getTermByToken(self, input_identifier):
        if type(input_identifier) == list:
            raise LookupError("Expected string, not list")

        return SimpleTerm(value=input_identifier,
                          title=self.message(input_identifier,
                                             self.inv_data[
                                                 input_identifier]))

    def getTerm(self, input_identifier):
        return self.getTermByToken(input_identifier)

    def getTerms(self):
        results = []
        identifiers = set()

        for (path, identifier) in self.data.items():
            if identifier in identifiers:
                continue

            identifiers.add(identifier)

            term = SimpleTerm(value=identifier,
                              title=self.message(identifier, path))
            results.append(term)

        return results


class PermissionsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        result = []
        sm = getSite().getSiteManager()

        for (permission, permission_object) in sm.getUtilitiesFor(IPermission):
            result.append(SimpleTerm(value=permission_object.id,
                                     title=_pmf(permission_object.title)))

        result.sort(key=lambda permission: permission.title)
        return SimpleVocabulary(result)


class LanguagesVocabulary(object):

    """Languages vocabulary."""

    implements(IVocabularyFactory)

    def __call__(self, context):
        portal = api.portal.get()
        terms = []
        portal_state = queryMultiAdapter(
            (portal, portal.REQUEST), name=u'plone_portal_state')
        languages = portal_state.locale().displayNames.languages
        for token, value in sorted(languages.iteritems()):
            terms.append(SimpleVocabulary.createTerm(
                token, token, value))

        return SimpleVocabulary(terms)
