import logging.config
import yaml
import os

def load_logging_conf():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(base_dir, "conf", "log.yaml")) as f:
        log_config = yaml.load(f)
        logging.config.dictConfig(log_config)

    return logging.getLogger("file")