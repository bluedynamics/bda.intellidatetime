Changes
=======

2.0.0 (2026-10-31)
------------------

- Drop the Python 2 remnants: ``IS_PY2`` and ``STRING_TYPES`` in
  ``bda.intellidatetime.converter``, ``u''`` prefixes and
  ``class X(object)``. Behaviour unchanged.
  [rnix]

- Use pytest as test runner. Move the tests to ``bda.intellidatetime.tests``
  and test the ``tzinfo`` normalization. The tests no longer depend on the
  wording of the ``datetime`` error message, which changed in Python 3.14.
  [rnix]

- Sort the imports with ruff (one per line, ``from`` imports first, no
  sections) and format the code with ``ruff format`` (90 characters per line,
  single quotes).
  [rnix]

- Add ``Makefile`` (mxmake) with ``qa.ruff``, ``qa.test`` and ``qa.coverage``
  domains, pin the ruff configuration in ``pyproject.toml`` and add a GitHub
  Actions test workflow.
  [rnix]

- Move the changelog from ``README.rst`` to ``CHANGES.rst``.
  [rnix]

- Refactor package layout to use ``pyproject.toml`` and implicit namespace
  packages.
  [rnix]

- Drop Python 2 support. Python >= 3.10 is required.
  [rnix]


1.4 (2022-12-05)
----------------

- Release wheel.
  [rnix]


1.3 (2018-07-16)
----------------

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]


1.2.2
-----

- Package cleanup.
  [rnix, 2017-03-29]


1.2.1
-----

- fix ``MANIFEST.in`` to include ``configure.zcml`` in release
  [jensens, 2013-09-23]


1.2
---

- Use ``zope.interface.implementer`` instead of ``zope.interface.implements``.
  [rnix, 2012-05-18]


1.1
---

- Provide convenience ``convert`` function.
  [rnix, 2010-05-08]

- Change package structure.
  [rnix, 2010-05-08]

- Move tests into seperate file.
  [rnix, 2010-05-08]

- Change signature of converter. could now be registered as utility as well if
  desired.
  [rnix, 2010-05-08]

- Adapter pattern deprecated.
  [rnix, 2010-05-08]


1.0
---

- Make it work
  [rnix, jensens]
