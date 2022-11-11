import io
import random
import threading

# from ruamel.yaml import YAML
from safe_ruamel import YAML

yaml = YAML()


yaml_samples = [
    """
---
 doe: "a deer, a female deer"
 ray: "a drop of golden sun"
 pi: 3.14159
 xmas: true
 french-hens: 3
 calling-birds:
   - huey
   - dewey
   - louie
   - fred
 xmas-fifth-day:
   calling-birds: four
   french-hens: 3
   golden-rings: 5
   partridges:
     count: 1
     location: "a pear tree"
   turtle-doves: two""",
    """
foo: bar
pleh: help
stuff:
  foo: bar
  bar: foo""",
    """
foo : bar
pleh : help
stuff : {'foo': 'bar', 'bar': 'foo'}""",
]

threads = []
loaded_yamls = []

concurrent = 4
times_inner = 500


def random_load_n_times(n):
    for _ in range(n):
        raw_yaml = random.choice(yaml_samples)
        loaded_yamls.append(yaml.load(io.StringIO(raw_yaml)))


def test_concurrent_use_yaml():
    for _ in range(concurrent):
        threads.append(t := threading.Thread(target=random_load_n_times, args=(times_inner,)))
        t.start()

    for t in threads:
        t.join()

    assert len(loaded_yamls) == concurrent * times_inner, f"Only loaded {len(loaded_yamls)} YAMLs"
