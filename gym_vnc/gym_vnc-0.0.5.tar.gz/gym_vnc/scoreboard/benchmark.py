import collections

class BenchmarkRegistry(object):
    def __init__(self, ):
        self.benchmarks = collections.OrderedDict()

    def add_benchmark(self, id, name, description):
        self.benchmarks[id] = {
            'id': id,
            'name': name,
            'description': description,
            'envs': [],
        }

    def add_task_to_benchmark(self, benchmark_id, env_id):
        self.benchmarks[benchmark_id]['envs'].append(env_id)

registry = BenchmarkRegistry()
add_benchmark = registry.add_benchmark
add_task_to_benchmark = registry.add_task_to_benchmark
