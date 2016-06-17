# Shared-Test-Automation-Resources

Add a private *pypi* repository in `~/.pypirc`:

```ini
[distutils]
index-servers = rallyhealth

[rallyhealth]
repository: https://artifacts.werally.in/artifactory/api/pypi/pypi-release-local
username: micah.enriquez
password: ***
```

Upload it to *artifactory* with:

```bash
python setup.py sdist upload -r rallyhealth
```
