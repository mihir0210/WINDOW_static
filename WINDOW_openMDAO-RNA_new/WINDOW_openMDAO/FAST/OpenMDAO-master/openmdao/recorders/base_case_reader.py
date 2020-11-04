"""
Base class for all CaseReaders.
"""


class BaseCaseReader(object):
    """
    Base class of all CaseReader implementations.

    Attributes
    ----------
    _format_version : int
        The version of the format assumed when loading the file.
    problem_metadata : dict
        Metadata about the problem, including the system hierachy and connections.
    solver_metadata : dict
        The solver options for each solver in the recorded model.
    system_metadata : dict
        Metadata about each system in the recorded model, including options and scaling factors.
    """

    def __init__(self, filename, pre_load=False):
        """
        Initialize.

        Parameters
        ----------
        filename : str
            The path to the file containing the recorded data.
        pre_load : bool
            If True, load all the data into memory during initialization.
        """
        self._format_version = None
        self.problem_metadata = {}
        self.solver_metadata = {}
        self.system_metadata = {}

    def get_cases(self, source, recurse=True, flat=False):
        """
        Iterate over the cases.

        Parameters
        ----------
        source : {'problem', 'driver', component pathname, solver pathname, iteration_coordinate}
            Identifies which cases to return.
        recurse : bool, optional
            If True, will enable iterating over all successors in case hierarchy
        flat : bool, optional
            If False and there are child cases, then a nested ordered dictionary
            is returned rather than an iterator.

        Returns
        -------
        list or dict
            The cases identified by source
        """
        pass

    def get_case(self, case_id, recurse=True):
        """
        Get case identified by case_id.

        Parameters
        ----------
        case_id : str or int
            The unique identifier of the case to return or an index into all cases.
        recurse : bool, optional
            If True, will return all successors to the case as well.

        Returns
        -------
        dict
            The case identified by case_id
        """
        pass

    def list_sources(self):
        """
        List of all the different recording sources for which there is recorded data.

        Returns
        -------
        list
            One or more of: `problem`, `driver`, `<component hierarchy location>`,
            `<solver hierarchy location>`
        """
        pass

    def list_source_vars(self, source):
        """
        List of all inputs and outputs recorded by the specified source.

        Parameters
        ----------
        source : {'problem', 'driver', component pathname, solver pathname}
            Identifies the source for which to return information.

        Returns
        -------
        dict
            {'inputs':[list of keys], 'outputs':[list of keys]}. Does not recurse.
        """
        pass
