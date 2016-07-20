# coding=utf-8
"""
说明: 数据模型的迁移 检查数据库字段是否有新增字段或者删除的字段
作者:pengxin.wu 15645060726@163.com
创建时间: 2016-7-3
"""


class Migrate(object):
    """
    用于迁移和检查数据
    """
    def __init__(self, model_cls):
        self.model = model_cls

    def update_field_redis(self):
        """
        更新存储在redis的模型字段
        :return:
        """
        app_name = self.model.Meta.app_name
        cls_name = self.model.__name__
        manager = self.model.objects
        # 获取模型的字段属性
        fields = getattr(self.model, "__fields_name")
        # 获取储存在redis中的所有字段
        key_name = "%(app_name)s.%(cls_name)s.fields" % {"app_name": app_name, "cls_name": cls_name}
        redis_fields_str = manager.redis.get(key_name)
        # 如果不存在的话 就需要在redis中设置这个键 用来存储 如果存在需要进行比较
        if not redis_fields_str:
            # 字段属性保存在列表中的 现在将其用.号进行连接转换成字符串保存到redis中去
            fields_str = ".".join(fields)
            self.model.objects.redis.set(key_name, fields_str)
            return True

        redis_fields_set = set(redis_fields_str.split("."))
        fields_set = set(fields)
        # 如果保存在redis的字段比模型字段中多 说明需要删除这个字段的相关内容
        ret = redis_fields_set - fields_set
        for field in ret:
            name = "{app_name}.{cls_name}.fields.{field}".format(app_name=app_name, cls_name=cls_name, field=field)
            manager.redis.delete(name)
            print "-->delete field %s" % name
        # 保存新的字段内容
        manager.redis.set(key_name, ".".join(fields))
        return True

    def start(self):
        """
        启动迁移
        :return:
        """
        self.update_field_redis()

# test
if __name__ == "__main__":
    # import __init__
    from manager import REDIS_CONNECT_SET
    REDIS_CONNECT_SET.update(dict(db=4, password="123456"))
    import test
    m = Migrate(test.Blog)
    m.update_field_redis()
