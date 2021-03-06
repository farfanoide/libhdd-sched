HDD Scheduling Algorithms Library
=================================
![travis status](https://travis-ci.org/farfanoide/libhdd-sched.svg?branch=master)
General purpose library for simulating various disk scheduling algorithms

Currently supported algorithms:
-------------------------------
- [ ] FIFO
- [ ] FCFS
- [ ] SCAN
- [ ] CSCAN
- [ ] LOOK
- [ ] CLOOK

Usage:
------

The interface is still being touched but ideally you should be able to
instantiate a simulation and run it like so:

```python
import json
import parsers
from lib.simulation import Simulation
example = json.loads(file.read(open('./examples/protosimulation.json')))
simulation = Simulation(example)
simulation.run('FCFS')
```

Dependencies:
-------------

Usage of virtualenv is encouraged.

Install dependencies from REQUIREMENTS via `pip`:

```bash
pip install -r REQUIREMENTS
```

Tests:
------

Navigate to the projects root directory and execute:

```bash
py.test
```

License:
--------

See the [LICENSE](LICENSE).

Contributing:
-------------

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

