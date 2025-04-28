import os
from glob import glob

import importlib_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("WEBHOOKS_VERSION", __version__),
        ("WEBHOOKS_PLUGIN_VERSION", ">=19.0.0,<20.0.0"),
    ]
)

########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorwebhooks/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutorwebhooks") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
