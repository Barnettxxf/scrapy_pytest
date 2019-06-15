import six


def compare(cond, op, data):
    if op == 'in' or op == 'keyin':
        if cond in data:
            return True
        return False
    elif op == 'eq':
        if cond == str(data):
            return True
        return False
    elif op == 'lt':
        if float(cond) - data < 0:
            return True
        return False
    elif op == 'gt':
        if float(cond) - data > 0:
            return True
        return False
    elif op == 'valuein':
        if isinstance(data, dict):
            for v in data.values():
                if cond in v:
                    return True
            return False
        elif isinstance(data, (tuple, list, six.string_types)):
            if cond in data:
                return True
            return False
        else:
            raise ValueError('Not support operation %s - %s - %s' % (cond, op, data))
    else:
        raise ValueError('Not support operation %s - %s - %s' % (cond, op, data))


class BaseFilter:
    base_factory = None

    def __init__(self, spider_cls, parse_func_name=None, settings=None):
        assert self.base_factory

        self.spider_cls = spider_cls
        self.factory = self.base_factory(spider_cls, settings)

        if parse_func_name:
            assert getattr(spider_cls, parse_func_name), f"{spider_cls.__name__} has not function {parse_func_name}"
            self._container = self._get_data()[parse_func_name]
        else:
            self._container = list(self._get_data().values())

    def _get_data(self):
        raise NotImplementedError

    def __getitem__(self, item):
        # There are supported operations, in, keyin, valuein, eq
        lst = item.split('__')
        if len(lst) != 3:
            raise ValueError('Must be this format: {condition}__{operation}__{attribute}, got %s', item)
        cond, op, attr = lst
        assert getattr(self._container[0], attr), "Not support filter(%s)" % item
        r = []
        for req_or_rsp in self._container:
            if compare(cond, op, getattr(req_or_rsp, attr)):
                r.append(req_or_rsp)
        return r
