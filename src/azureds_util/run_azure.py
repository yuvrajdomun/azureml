"""Azure Script Entry."""


from nodes.data_analytics import data_summary
from azureml.core import Run
import pandas as pd
import os
import joblib



if __name__ == "__main__":
    # entry point for running pip-installed projects
    # using `python -m <project_package>.run` command

    # Get the experiment run context
    
    #
    run = Run.get_context()

    # Get Data From input
    print("Loading Data...")
    data = run.input_datasets['iris'].to_pandas_dataframe()

    # load the diabetes dataset
    summury = data_summary(data)

    run.log_table(dict(summury))
    # Complete the run

    run.complete()
