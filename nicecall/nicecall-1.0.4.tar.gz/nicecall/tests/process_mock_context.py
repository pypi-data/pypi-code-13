import nicecall


class ProcessMockContext():
    def __init__(self, wrapped=None):
        self._wrapped = wrapped

    def __enter__(self):
        self._executed_args = []
        self._ignore_predicates = []
        self._keep_predicates = []
        self._on_stdout_actions = []
        self._on_stderr_actions = []
        return self

    def __exit__(self, type, value, tb):
        pass

    @property
    def mock(self):
        wrapped = self._wrapped or nicecall.tests.NullProcess

        class ProcessMock(wrapped):
            def execute(mock):
                self._executed_args.append(mock.args)
                return super(ProcessMock, mock).execute()

            def ignore(mock, predicate):
                self._ignore_predicates.append(predicate)
                return super(ProcessMock, mock).ignore(predicate)

            def keep(mock, predicate):
                self._keep_predicates.append(predicate)
                return super(ProcessMock, mock).keep(predicate)

            def on_stdout(mock, action):
                self._on_stdout_actions.append(action)
                return super(ProcessMock, mock).on_stdout(action)

            def on_stderr(mock, action):
                self._on_stderr_actions.append(action)
                return super(ProcessMock, mock).on_stderr(action)

        return ProcessMock

    @property
    def executed_args(self):
        return self._executed_args

    @property
    def ignore_predicates(self):
        return self._ignore_predicates

    @property
    def keep_predicates(self):
        return self._keep_predicates

    @property
    def on_stdout_actions(self):
        return self._on_stdout_actions

    @property
    def on_stderr_actions(self):
        return self._on_stderr_actions
