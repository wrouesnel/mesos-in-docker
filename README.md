# Mesos-in-Docker

This handy little environment is a way to stand up a Mesos environment to hack
on.

The included `app-manage.py` script can be used to add jobs to Marathon from
YAML-ized requested.

# All-in-one Image

The all-in-one image implements a full Mesos stack in a single Docker container.
Build/run it with `make run-allinone`.
