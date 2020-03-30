from typing import Any, Dict, List

import numpy as np

from kedro.io import AbstractDataSet
from msrest.exceptions import HttpOperationError
from azureml.core import Workspace, Datastore
from azureml.data.data_reference import DataReference

class AZblob_datastore_data(AbstractDataSet):
    """``ImageDataSet`` loads / save image data from a given filepath as `numpy` array using Pillow.

    Example:
    ::

        >>> ImageDataSet(filepath='/img/file/path.png')
    """

    def __init__(self,
                 container_path: str,
                 local_path : str,
                 credentials: Dict[str, Any] = None):
        """Creates a new instance of ImageDataSet to load / save image data at the given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        self._container_path = container_path
        self._local_path     = local_path
        self._credentials    = credentials

    def _load(self) -> np.ndarray:
        """Loads data from the image file.

        Returns:
            Data from the image file as a numpy array.
        """
        # Initialis Workspace

        ws = Workspace.from_config()

        blob_datastore_name = self._credentials['storage_name']
        account_name        = self._credentials['storage_name']   # Storage account name
        container_name      = self._credentials['container_name'] # Name of Azure blob container
        account_key         = self._credentials['key']            # Storage account key

        # Register a new datastore
        try:
            blob_datastore = blob_datastore = Datastore.get(ws, blob_datastore_name)
            print("Found Blob Datastore with name: %s" % blob_datastore_name)

        except HttpOperationError:
            blob_datastore = Datastore.register_azure_blob_container(workspace = ws, 
                                                                datastore_name = blob_datastore_name, 
                                                                container_name = container_name,
                                                                account_name = account_name,
        blob_datastore.download(target_path=self._local_path,
                                prefix=self._container_path,
                                show_progress=False)                                                    
        ...

    def _save(self, data: np.ndarray) -> None:
        """Saves image data to the specified filepath"""
        ...

    def _describe(self) -> Dict[str, Any]:
        
        """Returns a dict that describes the attributes of the dataset"""