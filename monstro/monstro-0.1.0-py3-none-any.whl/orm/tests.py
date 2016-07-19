# coding=utf-8

import uuid
import random

import tornado.gen
import tornado.testing
import tornado.ioloop

from bson.objectid import ObjectId

import monstro.testing

from . import fields, model, exceptions, queryset, manager


class FieldTest(monstro.testing.AsyncTestCase):

    def test_init(self):
        field = fields.IntegerField(default='1')

        self.assertEqual(field.default, '1')
        self.assertEqual(field.validators, [])

    def test_init__empty(self):
        field = fields.IntegerField()

        self.assertEqual(field.default, None)
        self.assertEqual(field.validators, [])

    @tornado.testing.gen_test
    def test__validation_error(self):
        field = fields.IntegerField()
        with self.assertRaises(exceptions.ValidationError):
            yield field.validate('a')

    @tornado.testing.gen_test
    def test__validation_error_required(self):
        field = fields.IntegerField(required=True)
        with self.assertRaises(exceptions.ValidationError):
            yield field.validate(None)

    @tornado.testing.gen_test
    def test__validation__validators(self):

        @tornado.gen.coroutine
        def validator(value):
            raise exceptions.ValidationError(value)

        field = fields.IntegerField(validators=[validator])

        with self.assertRaises(exceptions.ValidationError):
            yield field.validate(1)

    @tornado.testing.gen_test
    def test_not_implemented_error_on_call_is_valid(self):
        field = fields.Field()

        with self.assertRaises(NotImplementedError):
            yield field.validate(1)


class ModelTest(monstro.testing.AsyncTestCase):

    def test_init__empty(self):
        instance = model.Model()

        self.assertEqual({}, instance.__values__)
        self.assertEqual(None, instance.__cursor__)
        self.assertFalse(hasattr(instance, 'objects'))

    def test_new(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            name = fields.StringField()

        instance = CustomModel()

        self.assertEqual('test', CustomModel.__collection__)
        self.assertEqual(CustomModel.objects.model, CustomModel)
        self.assertIn('name', instance.__fields__)
        self.assertIn('_id', instance.__fields__)

    def test_new_init_with__id_field(self):
        with self.assertRaises(AttributeError):

            class Test(model.Model):
                __collection__ = 'test'
                _id = fields.IntegerField()

    @tornado.testing.gen_test
    def test_getattr__attribute_error(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            name = fields.StringField()

        instance = CustomModel(name='test')

        with self.assertRaises(AttributeError):
            instance.none()

    @tornado.testing.gen_test
    def test_data(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            name = fields.StringField()

        instance = CustomModel(name='test')

        self.assertEqual(
            {'name': 'test', '_id': None}, (yield instance.to_internal_value())
        )

    @tornado.testing.gen_test
    def test_save(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()

        instance = CustomModel(string=uuid.uuid4().hex)
        yield instance.save()

        _model = yield instance.objects.get(string=instance.string)

        self.assertEqual(instance.string, _model.string)

    @tornado.testing.gen_test
    def test_update(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()

        instance = CustomModel(string=uuid.uuid4().hex)
        yield instance.save()

        yield instance.update(string='test')

        self.assertEqual('test', instance.string)

    @tornado.testing.gen_test
    def test_refresh(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()

        instance = CustomModel(string=uuid.uuid4().hex)
        yield instance.save()

        _instance = yield instance.objects.get(_id=instance._id)
        yield _instance.update(string=uuid.uuid4().hex)

        self.assertNotEqual(instance.string, _instance.string)

        yield instance.refresh()

        self.assertEqual(instance.string, _instance.string)

    @tornado.testing.gen_test
    def test_resave(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()

        instance = yield CustomModel.objects.create(string=uuid.uuid4().hex)

        instance.string = uuid.uuid4().hex
        yield instance.save()

        _model = yield instance.objects.get(string=instance.string)

        self.assertEqual(instance.string, _model.string)

    @tornado.testing.gen_test
    def test_construct(self):
        class RelatedModel(model.Model):
            __collection__ = 'test2'

            name = fields.StringField()

        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()
            related = fields.ForeignKeyField(
                related_model=RelatedModel, related_field='name'
            )

        related_model = RelatedModel(name=uuid.uuid4().hex)
        yield related_model.save()

        instance = CustomModel(string=uuid.uuid4().hex, related=related_model)
        yield instance.save()

        instance = yield instance.objects.get(string=instance.string)

        self.assertEqual(related_model.name, instance.related.name)

    @tornado.testing.gen_test
    def test_validate(self):
        class RelatedModel(model.Model):
            __collection__ = 'test2'

            name = fields.StringField()

        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()
            related = fields.ForeignKeyField(
                related_model=RelatedModel, related_field='name'
            )

        related_model = RelatedModel(name=uuid.uuid4().hex)
        yield related_model.save()

        instance = CustomModel(string=uuid.uuid4().hex, related=related_model)
        instance.related = 'wrong'

        with self.assertRaises(exceptions.ValidationError):
            yield instance.save()

        try:
            yield instance.save()
        except exceptions.ValidationError as e:
            self.assertIn('related', e.error)

    @tornado.testing.gen_test
    def test_validate__unique(self):

        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField(unique=True)

        instance = yield CustomModel.objects.create(string=uuid.uuid4().hex)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield CustomModel.objects.create(string=instance.string)

        self.assertEqual(
            context.exception.error['string'],
            fields.Field.default_error_messages['unique']
        )

    @tornado.testing.gen_test
    def test_delete(self):
        class CustomModel(model.Model):
            __collection__ = 'test'

            string = fields.StringField()

        instance = CustomModel(string=uuid.uuid4().hex)
        yield instance.save()
        yield instance.delete()

        with self.assertRaises(instance.DoesNotExist):
            yield instance.objects.get(string=instance.string)

    @tornado.testing.gen_test
    def test_custom_manager(self):
        class CustomManager(manager.Manager):

            @tornado.gen.coroutine
            def create(self, **kwargs):
                raise tornado.gen.Return(None)

        class CustomModel(model.Model):
            __collection__ = 'test'
            objects = CustomManager()

            string = fields.StringField()

        instance = yield CustomModel.objects.create()

        self.assertFalse(instance)


class ChoiceTest(monstro.testing.AsyncTestCase):

    def test(self):
        choices = model.Choice(('TEST', 'value', 'Description'))

        self.assertEqual(choices.TEST, 'value')

    def test__attribute_error(self):
        choices = model.Choice(('TEST', 'value', 'Description'))

        with self.assertRaises(AttributeError):
            self.__ = choices.NONE

    def test_contains(self):
        choices = model.Choice(('TEST', 'value', 'Description'))

        self.assertTrue('value' in choices)


class ManagerTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def setUpHelper(self):
        class Test(model.Model):

            __collection__ = uuid.uuid4().hex

            name = fields.StringField()

        self.model = Test

        self.number = random.randint(10, 20)

        for i in range(self.number):
            yield self.model.objects.create(name='test{}'.format(i))

    @tornado.testing.gen_test
    def test_filter(self):
        count = yield (yield self.model.objects.filter()).count()

        self.assertEqual(self.number, count)

    @tornado.testing.gen_test
    def test_filter_with_query(self):
        count = yield (yield self.model.objects.filter(name='test10')).count()

        self.assertEqual(1, count)

    @tornado.testing.gen_test
    def test_create(self):
        instance = yield self.model.objects.create(name='New')
        count = yield (
            yield self.model.objects.filter(name=instance.name)
        ).count()

        self.assertEqual(1, count)


class QuerySetTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def setUpHelper(self):
        class Test(model.Model):

            __collection__ = uuid.uuid4().hex

            name = fields.StringField()

        self.model = Test
        self.queryset = queryset.QuerySet(self.model)

        self.number = random.randint(10, 20)

        for i in range(self.number):
            yield self.model.objects.create(name='test{}'.format(i))

    def test_init(self):
        self.assertEqual(self.model, self.queryset.model)

    @tornado.testing.gen_test
    def test_filter(self):
        count = yield (yield self.queryset.filter()).count()

        self.assertEqual(self.number, count)

    @tornado.testing.gen_test
    def test_first_last(self):
        first = yield (yield self.queryset.filter()).first()
        last = yield (yield self.queryset.filter()).last()

        self.assertTrue(first.name < last.name)

    @tornado.testing.gen_test
    def test_filter_with_query(self):
        count = yield (yield self.queryset.filter(name='test0')).count()

        self.assertEqual(1, count)

    @tornado.testing.gen_test
    def test_all(self):
        items = yield (yield self.queryset.filter()).all()

        self.assertEqual(self.number, len(items))

    @tornado.testing.gen_test
    def test_slice(self):
        items = yield (yield self.queryset.filter())[1:7]

        self.assertEqual(6, len(items))

    @tornado.testing.gen_test
    def test_slice_by_items(self):
        yield (yield self.queryset.filter()).all()
        items = yield self.queryset[1:7]

        self.assertEqual(6, len(items))

    @tornado.testing.gen_test
    def test_slice_left(self):
        number = random.randint(5, 7)

        items = yield (yield (yield self.queryset.filter())[number:]).all()

        self.assertEqual(self.number - number, len(items))

    @tornado.testing.gen_test
    def test_slice_right(self):
        number = random.randint(5, 7)

        items = yield (yield (yield self.queryset.filter())[:number]).all()

        self.assertEqual(number, len(items))

    @tornado.testing.gen_test
    def test_slice_index(self):
        number = random.randint(5, 7)

        instance = yield (yield self.queryset.filter())[number]

        self.assertEqual('test{}'.format(number), instance.name)


class BooleanFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.BooleanField()
        self.assertTrue((yield field.validate(True)))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.BooleanField()

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.BooleanField.default_error_messages['invalid']
        )


class StringFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.StringField()
        self.assertEqual('Test', (yield field.validate('Test')))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.StringField()

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate(10)

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__min_length(self):
        field = fields.StringField(min_length=5, default='test')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['min_length'].format(
                field
            )
        )

    @tornado.testing.gen_test
    def test_validate__max_length(self):
        field = fields.StringField(max_length=3, default='test')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['max_length'].format(
                field
            )
        )


class IntegerFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.IntegerField()
        self.assertEqual(10, (yield field.validate('10')))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.IntegerField()

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.IntegerField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__min_value(self):
        field = fields.IntegerField(default=10, min_value=11)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['min_value'].format(
                field
            )
        )

    @tornado.testing.gen_test
    def test_validate__max_value(self):
        field = fields.IntegerField(default=10, max_value=9)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['max_value'].format(
                field
            )
        )


class FloatFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.FloatField()
        self.assertEqual(10.2, (yield field.validate('10.2')))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.FloatField()

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.FloatField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__min_value(self):
        field = fields.FloatField(default=10.1, min_value=10.2)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['min_value'].format(
                field
            )
        )

    @tornado.testing.gen_test
    def test_validate__max_value(self):
        field = fields.FloatField(default=10.11, max_value=10.10)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.NumericField.default_error_messages['max_value'].format(
                field
            )
        )


class ChoiceFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.ChoiceField(choices=['a', 'b'])
        self.assertEqual('a', (yield field.validate('a')))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.ChoiceField(default='c', choices=['a', 'b'])

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ChoiceField.default_error_messages['invalid'].format(field)
        )


class MultipleChoiceFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.MultipleChoiceField(choices=['a', 'b'])
        self.assertEqual(['a'], (yield field.validate(['a'])))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.MultipleChoiceField(default='c', choices=['a', 'b'])

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['invalid'].format(field)
        )

    @tornado.testing.gen_test
    def test_validate__choices(self):
        field = fields.MultipleChoiceField(default=['c'], choices=['a', 'b'])

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MultipleChoiceField \
                .default_error_messages['choices'].format(field)
        )


class ArrayFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.ArrayField(field=fields.IntegerField())
        self.assertEqual([10], (yield field.validate(['10'])))

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.ArrayField(default='string')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['invalid'].format(field)
        )

    @tornado.testing.gen_test
    def test_validate__invalid_item(self):
        field = fields.ArrayField(default=['j'], field=fields.IntegerField())

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ArrayField.default_error_messages['child'].format(
                index=0,
                message=fields.IntegerField.default_error_messages['invalid']
            )
        )


class URLFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.URLField()
        self.assertEqual(
            'https://pyvim.com/about/',
            (yield field.validate('https://pyvim.com/about/'))
        )

    @tornado.testing.gen_test
    def test_validate__invalid_type(self):
        field = fields.URLField(default=5)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.URLField(default=':/wrong')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.URLField.default_error_messages['url']
        )


class HostFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate_ip(self):
        field = fields.HostField()
        self.assertEqual(
            '144.76.78.182', (yield field.validate('144.76.78.182'))
        )

    @tornado.testing.gen_test
    def test_validate_url(self):
        field = fields.HostField()
        self.assertEqual('pyvim.com', (yield field.validate('pyvim.com')))

    @tornado.testing.gen_test
    def test_validate__invalid_type(self):
        field = fields.HostField(default=5)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.StringField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__invalid(self):
        field = fields.HostField(default=':/wrong')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.HostField.default_error_messages['pattern'].format(field)
        )


class MapFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.MapField()
        self.assertEqual(
            {'key': 'value'}, (yield field.validate({'key': 'value'}))
        )

    @tornado.testing.gen_test
    def test_validate__invalid_json(self):
        field = fields.MapField(default='wrong')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MapField.default_error_messages['invalid'].format(field)
        )

    @tornado.testing.gen_test
    def test_validate__invalid_type(self):
        field = fields.MapField(default=5)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.MapField.default_error_messages['invalid'].format(field)
        )


class SlugFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.SlugField()
        self.assertEqual(
            'back-jack-100_1', (yield field.validate('back-jack-100_1'))
        )

    @tornado.testing.gen_test
    def test_validate__error(self):
        field = fields.SlugField(default='wrong slug')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.SlugField.default_error_messages['pattern'].format(field)
        )


class IDFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_to_representation(self):
        field = fields.IDField()

        value = yield field.to_representation(str(ObjectId()))

        self.assertIsInstance(value, ObjectId)

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.IDField(default=ObjectId())

        yield field.validate()

    @tornado.testing.gen_test
    def test_is_valid__from_string(self):
        field = fields.IDField()

        yield field.is_valid(str(ObjectId()))

    @tornado.testing.gen_test
    def test_is_valid__from_string_error(self):
        field = fields.IDField()

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.is_valid('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.IDField.default_error_messages['invalid']
        )

    @tornado.testing.gen_test
    def test_validate__error(self):
        field = fields.IDField(default='blackjack')

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.IDField.default_error_messages['invalid']
        )


class RelatedModelFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def setUpHelper(self):
        class Test(model.Model):

            __collection__ = uuid.uuid4().hex

            name = fields.StringField()

        self.model = Test
        self.instance = yield self.model.objects.create(name=uuid.uuid4().hex)

    @tornado.testing.gen_test
    def test_to_representation(self):
        field = fields.RelatedModelField(
            default={'name': 'Test'}, related_model=self.model
        )
        value = yield field.to_representation(field.default)

        self.assertEqual(value.name, 'Test')

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.RelatedModelField(
            default=self.instance, related_model=self.model
        )
        yield field.validate()

    @tornado.testing.gen_test
    def test_validate__error(self):
        field = fields.RelatedModelField(
            default='blackjack', related_model=self.model
        )

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.RelatedModelField.default_error_messages['invalid'].format(
                field
            )
        )


class ForeignKeyFieldTest(monstro.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def setUpHelper(self):
        class Test(model.Model):

            __collection__ = uuid.uuid4().hex

            name = fields.StringField()

        self.model = Test
        self.instance = yield self.model.objects.create(name=uuid.uuid4().hex)

    @tornado.testing.gen_test
    def test_to_representation(self):
        field = fields.ForeignKeyField(
            default=self.instance.name, related_model=self.model,
            related_field='name'
        )
        value = yield field.to_representation(field.default)

        self.assertEqual(value.name, self.instance.name)

    @tornado.testing.gen_test
    def test_to_representation__from_string_id(self):
        field = fields.ForeignKeyField(related_model=self.model)
        value = yield field.to_representation(str(self.instance._id))

        self.assertEqual(value.name, self.instance.name)

    @tornado.testing.gen_test
    def test_to_representation__from_string_id_error(self):
        field = fields.ForeignKeyField(related_model=self.model)

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.to_representation('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.ForeignKeyField.default_error_messages['foreign_key']
        )

    @tornado.testing.gen_test
    def test_to_representation__does_not_exist(self):
        field = fields.ForeignKeyField(
            related_model=self.model, related_field='name'
        )

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.to_representation('blackjack')

        self.assertEqual(
            context.exception.error,
            fields.ForeignKeyField.default_error_messages['foreign_key']
        )

    @tornado.testing.gen_test
    def test_validate(self):
        field = fields.ForeignKeyField(
            default=self.instance, related_model=self.model,
            related_field='name'
        )
        yield field.validate()

        self.assertIsInstance(self.instance, self.model)

    @tornado.testing.gen_test
    def test_is_valid(self):
        field = fields.ForeignKeyField(
            related_model=self.model, related_field='name'
        )
        yield field.is_valid(self.instance)

        self.assertIsInstance(self.instance, self.model)

    @tornado.testing.gen_test
    def test_to_internal_value__id(self):
        field = fields.ForeignKeyField(related_model=self.model)

        value = yield field.to_internal_value(self.instance)

        self.assertEqual(str(self.instance._id), value)

    @tornado.testing.gen_test
    def test_validate__from_key(self):
        field = fields.ForeignKeyField(
            default=self.instance.name, related_model=self.model,
            related_field='name'
        )
        yield field.validate()

        self.assertIsInstance(self.instance, self.model)

    @tornado.testing.gen_test
    def test_validate__error(self):
        field = fields.ForeignKeyField(
            default='blackjack', related_model=self.model, related_field='name'
        )

        with self.assertRaises(exceptions.ValidationError) as context:
            yield field.validate()

        self.assertEqual(
            context.exception.error,
            fields.ForeignKeyField.default_error_messages['foreign_key']
        )
