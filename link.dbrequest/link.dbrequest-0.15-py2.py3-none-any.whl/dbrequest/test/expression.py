# -*- coding: utf-8 -*-

from b3j0f.utils.ut import UTCase
from unittest import main

from link.dbrequest.expression import E, F
from link.dbrequest.comparison import C


class ExpressionTest(UTCase):
    def test_simple_expr(self):
        e = E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'ref',
                'val': 'propname'
            }
        )

    def test_expr_add(self):
        e = E('propname') + 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_add',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 + E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_add',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_sub(self):
        e = E('propname') - 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_sub',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 - E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_sub',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_mul(self):
        e = E('propname') * 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_mul',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 * E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_mul',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_div(self):
        e = E('propname') / 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_div',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 / E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_div',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_pow(self):
        e = E('propname') ** 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_pow',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 ** E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_pow',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_lshift(self):
        e = E('propname') << 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_lshift',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 << E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_lshift',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_rshift(self):
        e = E('propname') >> 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_rshift',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 >> E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_rshift',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_and(self):
        e = E('propname') & 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_and',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 & E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_and',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_or(self):
        e = E('propname') | 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_or',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 | E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_or',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_xor(self):
        e = E('propname') ^ 5
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_xor',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'val',
                        'val': 5
                    }
                ]
            }
        )

        e = 5 ^ E('propname')
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_xor',
                'val': [
                    {
                        'name': 'val',
                        'val': 5
                    },
                    {
                        'name': 'ref',
                        'val': 'propname'
                    }
                ]
            }
        )

    def test_expr_func(self):
        e = F('funcname', E('propname'), E('propname') * 5)
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'func_funcname',
                'val': [
                    {
                        'name': 'ref',
                        'val': 'propname'
                    },
                    {
                        'name': 'op_mul',
                        'val': [
                            {
                                'name': 'ref',
                                'val': 'propname'
                            },
                            {
                                'name': 'val',
                                'val': 5
                            }
                        ]
                    }
                ]
            }
        )

    def test_in_condition(self):
        c = C('prop1') == E('prop2')
        ast = c.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'prop1'
                    },
                    {
                        'name': 'ref',
                        'val': 'prop2'
                    }
                ]
            }
        )

        c = C('prop1') == (E('prop2') + E('prop3'))
        ast = c.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'cond_eq',
                'val': [
                    {
                        'name': 'prop',
                        'val': 'prop1'
                    },
                    {
                        'name': 'op_add',
                        'val': [
                            {
                                'name': 'ref',
                                'val': 'prop2'
                            },
                            {
                                'name': 'ref',
                                'val': 'prop3'
                            }
                        ]
                    }
                ]
            }
        )

    def test_complex_expr(self):
        e = (E('foo') + E('bar')) + (E('baz') + E('biz'))
        ast = e.get_ast()

        self.assertEqual(
            ast,
            {
                'name': 'op_add',
                'val': [
                    {
                        'name': 'op_add',
                        'val': [
                            {
                                'name': 'ref',
                                'val': 'foo'
                            },
                            {
                                'name': 'ref',
                                'val': 'bar'
                            }
                        ]
                    },
                    {
                        'name': 'op_add',
                        'val': [
                            {
                                'name': 'ref',
                                'val': 'baz'
                            },
                            {
                                'name': 'ref',
                                'val': 'biz'
                            }
                        ]
                    }
                ]
            }
        )


if __name__ == '__main__':
    main()
