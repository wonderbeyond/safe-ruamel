# Safe ruamel.yaml

A proxy class for ruamel.yaml.YAML that bypass the thread-safe issue.

---

## Usage

```python
from safe_ruamel import YAML

yaml = YAML()

obj = yaml.load("a: 1")
print(yaml.dump(obj).read())
```
