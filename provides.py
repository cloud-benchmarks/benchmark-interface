from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class BenchmarkProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:benchmark}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.required')
        required_keys = [
            'hostname',
            'port',
            'api_port'
        ]

        # Check the relation data
        config = {}
        for key in self.required_keys:
            val = relation_get(key)
            if val is not None:
                config[key] = val
            else:
                # We don't have all of the required keys
                config = {}
                break

        if len(config):
            with open('/etc/benchmark.conf', 'w') as f:
                for key, val in iter(config.items()):
                    f.write("%s=%s\n" % (key, val))


    @hook('{provides:benchmark}-relation-{broken,departed}')
    def broken(self):
        self.remove_state('{relation_name}.required')

    def benchmarks(self, benchmarks):
        relation_info = {
            'benchmarks': ','.join(benchmarks),
        }

        self.set_remote(**relation_info)
