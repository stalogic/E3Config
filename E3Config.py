import json

class E3Config(object):
    def __init__(self, config_path, targets=[]):
        self._config = dict()
        self._targets = targets
        with open(config_path, "r") as fr:
            raw_config = json.load(fr)
        self._parse_fields(raw_config, None)
        self._gen_fields(raw_config)

    def _parse_fields(self, raw_config, domain):
        for key in [key for key in raw_config if not isinstance(raw_config[key], dict)]:
            if key not in self._config:
                self._config[key] = raw_config[key]
            elif domain in self._targets:
                self._config[key] = raw_config[key]
        
        for key in [key for key in raw_config if isinstance(raw_config[key], dict) and not key.startswith("_")]:
            self._parse_fields(raw_config[key], key)

    def _gen_fields(self, raw_config):
        gen_rules = [key for key in raw_config if key.startswith("_")]
        for index, rule_level in enumerate(sorted(gen_rules)):
            for field in raw_config[rule_level]:
                func = getattr(self, raw_config[rule_level][field]["rule"])
                value = func(*raw_config[rule_level][field]["args"])
                self._config[field] = value
                for domain in [for key in raw_config[rule_level][field] if key not in ("rule", "args")]:
                    if domain in self._targets:
                        func = getattr(self, raw_config[rule_level][field][domain]['rule'])
                        value = func(*raw_config[rule_level][field][domain]["args"])
                        self._config[field] = value

    def calc(self, *ops):
        return calc_with_rpn(self._config, *ops)
    
    def concat(self, *args):
        return concat(self._config, *args)

    def concat_with_flag(self, *args):
        return concat_with_flag(self._config, *args)
