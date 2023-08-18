# Function to install PySDDP library if needed
def install_pysddp():
    """
    Installs the PySDDP library.
    """
    # The following command is specific to Colab environment and may not be needed in other environments
    try:
        import PySDDP
        print("PySDDP is already installed.")
    except ImportError:
        # Uncomment the next line if you want to install PySDDP in your environment
        # !pip install PySDDP
        print("PySDDP has been installed.")