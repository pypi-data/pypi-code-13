import unittest

from dici import dici
from robber import expect


class DiciTest(unittest.TestCase):

    def test_instantiate_dici_with_keyword_arguments(self):
        dictionary = dici(foo='bar', fizz='buzz')
        expect(dictionary.foo).to.eq('bar')
        expect(dictionary.fizz).to.eq('buzz')

    def test_handles_setting_fields_to_dictionary_values(self):
        dictionary = dici()
        dictionary.foo = {
            'bar': True
        }
        expect(dictionary.foo.bar).to.be.true()

    def test_compare_a_dici_with_a_dictionary(self):
        dictionary = dici(foo='bar', fizz='buzz')
        expect(dictionary == {
            'foo': 'bar',
            'fizz': 'buzz'
        }).to.be.true()

    def test_get_field_value_from_dici_with_dot_notation(elf):
        dictionary = dici()
        dictionary.foo = {
            'bar': 'baz',
            'fizz': 'buzz'
        }
        expect(dictionary.foo.bar).to.eq('baz')

    def test_get_field_value_from_dici_with_dot_notation_within_index_notation(self):
        dictionary = dici()
        dictionary.foo = {
            'bar': 'baz',
            'fizz': 'buzz'
        }
        expect(dictionary['foo.bar']).to.eq('baz')

    def test_add_field_to_dici_with_dot_notation(self):
        dictionary = dici()
        dictionary.foo = 'bar'
        expect(dictionary.foo).to.eq('bar')

    def test_add_field_to_dici_with_index_notation(self):
        dictionary = dici()
        dictionary['foo'] = 'bar'
        expect(dictionary.foo).to.eq('bar')

    def test_delete_field_to_dici_with_dot_notation_within_index_notation(self):
        dictionary = dici()
        dictionary.foo = {
            'bar': 'baz',
            'fizz': 'buzz'
        }
        del dictionary['foo.bar']
        expect(dictionary).to.eq({
            'foo': {
                'fizz': 'buzz' 
            }
        })

    def test_delete_field_from_dici_with_dot_notation(self):
        dictionary = dici(foo='bar', fizz='buzz')
        del dictionary.foo
        expect(dictionary).to.eq({
            'fizz': 'buzz'
        })

    def test_check_dici_contains_key_element_with_in_expression(self):
        dictionary = dici(foo='bar', fizz='buzz')
        expect('foo' in dictionary).to.be.true()
        expect('fizz' in dictionary).to.be.true()

    def test_can_iterate_over_the_keys_of_a_dici(self):
        dictionary = dici(foo='bar', fizz='buzz')
        results = []
        for key in dictionary:
            results.append(key)
        expect(results).to.eq(['foo', 'fizz'])

    def test_dici_set_for_regular_field(self):
        dictionary = dici()
        dictionary.set('foo', 'bar')
        expect(dictionary.foo).to.eq('bar')

    def test_dici_set_for_regular_nested_field(self):
        dictionary = dici()
        dictionary.set('foo.bar', 'buzz')
        expect(dictionary.foo.bar).to.eq('buzz')
