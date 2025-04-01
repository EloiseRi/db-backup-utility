import logging
import yaml

logger = logging.getLogger(__name__)

def set_config(config_file):
    try:
        with open(config_file, "r") as yamlfile:
            cfg = yaml.safe_load(yamlfile)

        required_keys = [ "database", "backup", "cloud", "notifications" ]

        for key in required_keys:
            if key not in cfg:
                raise ValueError(f"Missing required configuration key: {key}.")
            
        if "cloud" in cfg:
            aws_enabled = cfg["cloud"].get("aws", {}).get("enabled", False)
            gcp_enabled = cfg["cloud"].get("gcp", {}).get("enabled", False)

            if not aws_enabled and not gcp_enabled:
                logger.warning(f"There is no cloud configuration enabled, backup will be locally stored.")

        return cfg

    except ValueError as e:
        logger.error(f"Configuration error: {e}.")
