import logging.config
import os
import sys
from pathlib import Path

from IPython.core.magic import register_line_magic

# Find the project root (./../../../)
startup_error = None
project_path = Path(__file__).parents[3].resolve()


@register_line_magic
def reload_kedro(path, line=None):
    """"Line magic which reloads all Kedro default variables."""
    global startup_error
    global context
    global catalog

    try:
        import kedro.config.default_logger
        from kedro.context import KEDRO_ENV_VAR, load_context
        from kedro.cli.jupyter import collect_line_magic
    except ImportError:
        logging.error(
            "Kedro appears not to be installed in your current environment "
            "or your current IPython session was not started in a valid Kedro project."
        )
        raise

    try:
        path = path or project_path
        logging.debug("Loading the context from %s", str(path))

        context = load_context(path, env=os.getenv(KEDRO_ENV_VAR))
        catalog = context.catalog

        # remove cached user modules
        package_name = context.__module__.split(".")[0]
        to_remove = [mod for mod in sys.modules if mod.startswith(package_name)]
        for module in to_remove:
            del sys.modules[module]

        logging.info("** Kedro project %s", str(context.project_name))
        logging.info("Defined global variable `context` and `catalog`")

        for line_magic in collect_line_magic():
            register_line_magic(line_magic)
            logging.info("Registered line magic `%s`", line_magic.__name__)
    except Exception as err:
        startup_error = err
        logging.exception(
            "Kedro's ipython session startup script failed:\n%s", str(err)
        )
        raise err

@register_line_magic
def reload_azureml_ws(line=None):
    global ws
    global conf_catalog
    try:
        import azureml.core
        from azureml.core import Workspace
    except ImportError:
        logging.error(
            "azureml appears not to be installed in your current environment "
        )
        raise

    # Load the workspace from the saved config file
    try:
        ws = Workspace.from_config()
        print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))
        print('Imported workspace as ws')
    except:
        logging.error(
            "Azureml Workspace appear to not exist, please make sure workspace has been created and config in right folder. "
        )
        raise
    # Load Credentials
    try:
        from kedro.config import ConfigLoader

        conf_paths = ["conf/base", "conf/local"]
        conf_loader = ConfigLoader(conf_paths)
        conf_catalog = conf_loader.get("credentials*")
    except:
        logging.error(
            "Failed to laod config from kedro.config"
        )
        raise
    logging.info("Defined global variable `ws` and `conf_catalog`")

reload_kedro(project_path)
