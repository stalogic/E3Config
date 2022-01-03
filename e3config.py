import json

def calc_with_rpn(var_dict, *args):
    ops = ["+", "-", "*", "/", "//"]
    stack = []
    for o in args:
        if o in ops:
            a = stack.pop()
            b = stack.pop()
            if o == "+":
                stack.append(a+b)
            elif o == "-":
                stack.append(b-a)
            elif o == "*":
                stack.append(a*b)
            elif o == "/":
                stack.append(b/a)
            elif o == "//":
                stack.append(b//a)
            else:
                raise "Unsupported op"
        else:
            if o in var_dict:
                stack.append(var_dict[o])
            elif o.replace(".", "1", 1).isdigit():
                stack.append(eval(o))
            else:
                raise "Field not exists"
    return stack.pop()
            

class E3Config(object):
    def __init__(self, config_path, targets=[]):
        self._config = dict()
        self._targets = targets
        with open(config_path, "r") as fr:
            raw_config = json.load(fr)
        self._parse_fields(raw_config, None)
        self._gen_fields(raw_config)

    def get_config(self):
        return self._config

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
                for domain in [key for key in raw_config[rule_level][field] if key not in ("rule", "args")]:
                    if domain in self._targets:
                        func = getattr(self, raw_config[rule_level][field][domain]['rule'])
                        value = func(*raw_config[rule_level][field][domain]["args"])
                        self._config[field] = value

    def calc(self, *ops):
        return calc_with_rpn(self._config, *ops)
    
    def concat(self, *args):
        delimiter = args[0]
        args = args[1:]
        arr = []
        for e in args:
            if e not in self._config:
                if e.startswith("`") and e.endswith("`"):
                    arr.append(e[1:-1])
                else:
                    print("Undefine key: {} in rule: {}, args:{}".format(e, "concat", args))
                    raise "Constant value should surrounded with '`'"
            else:
                arr.append(str(self._config[e]))
        return delimiter.join(arr)

    def concat_with_flag(self, *args):
        delimiter = args[0]
        args = args[1:]
        arr = []
        for arg in args:
            key, flag = arg.split(":")
            arr.append(flag+str(self._config[key]))
        return delimiter.join(arr)
