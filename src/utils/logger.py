import logging
import logging.handlers
import os
import utils.config as config

# Configura o logger central 'universe'
logger = logging.getLogger('universe')
if not logger.handlers:
    level_name = getattr(config, 'LOG_LEVEL', 'DEBUG')
    level = getattr(logging, level_name.upper(), logging.DEBUG)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    if getattr(config, 'DEBUG_LOG', False):
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler (rotating)
        log_file = getattr(config, 'LOG_FILE', 'universe_debug.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

# Expose function to get the logger if needed
def get_logger():
    return logger
