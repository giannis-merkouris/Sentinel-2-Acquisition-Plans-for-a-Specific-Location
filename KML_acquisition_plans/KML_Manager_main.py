import logging
import json
import os
import autoroot
from datetime import datetime
from KML_acquisition_plans.KML_Manager_class import KMLManager

def job(config_file_path):
    logging.info("Running scheduled task...")

    # Check if the config file exists
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as config_file:
                config = json.load(config_file)
                
            # Retrieve directories from the config file
            base_directory = config.get("base_directory")
            s2a_directory = config.get("s2a_directory")
            s2b_directory = config.get("s2b_directory")
            s2c_directory = config.get("s2c_directory")
            logging.info(f'Config found. Using directories: base={base_directory}, S2A={s2a_directory}, S2B={s2b_directory}, S2C={s2c_directory}')

            # Create KMLManager with directories from config
            kml_manager = KMLManager(base_directory, s2a_directory, s2b_directory, s2c_directory)
        except Exception as e:
            logging.error(f'Failed to read config file: {e}')
            # Fallback to default initialization if there's an error
            kml_manager = KMLManager() # Use default directories
    else:
        logging.warning(f'Config file {config_file_path} not found. Using default directories.')
        # Fallback to default initialization if config doesn't exist
        kml_manager = KMLManager() # Use default directories

    # Download the KML files and update the local dataset
    try:
        kml_manager.delete_kml_in_UpdateFile()
        kml_manager.download_kml()
        kml_manager.update_local_dataset()
    except Exception as e:
        logging.error(f'An error occurred during the scheduled task: {e}')

if __name__ == "__main__":
    # Generate a timestamped log file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'KML_acquisition_plans/log_archive/test_kml_main{timestamp}.log'

    # Set up logging to append to the existing log file instead of overwriting it
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'  # 'a' ensures that the log file is appended to, not overwritten
    )

    logging.info("Starting the scheduled task...")

    # Path to the configuration file
    config_file_path = 'configs/config_KML_directories.json'

    # Run the job
    job(config_file_path)
