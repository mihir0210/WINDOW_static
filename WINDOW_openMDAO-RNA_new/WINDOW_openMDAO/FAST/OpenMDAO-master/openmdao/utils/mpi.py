"""A bunch of MPI utilities."""

from contextlib import contextmanager
import io
import os
import sys
import traceback
import unittest

from six import PY3

from openmdao.core.analysis_error import AnalysisError


def _redirect_streams(to_fd):
    """
    Redirect stdout/stderr to the given file descriptor.

    Based on: http://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/.

    Parameters
    ----------
    to_fd : int
        File descriptor to redirect to.
    """
    original_stdout_fd = sys.stdout.fileno()
    original_stderr_fd = sys.stderr.fileno()

    # Flush and close sys.stdout/err - also closes the file descriptors (fd)
    sys.stdout.close()
    sys.stderr.close()

    # Make original_stdout_fd point to the same file as to_fd
    os.dup2(to_fd, original_stdout_fd)
    os.dup2(to_fd, original_stderr_fd)

    # Create a new sys.stdout that points to the redirected fd
    if PY3:
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))
        sys.stderr = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))
    else:
        sys.stdout = os.fdopen(original_stdout_fd, 'wb', 0)  # 0 makes them unbuffered
        sys.stderr = os.fdopen(original_stderr_fd, 'wb', 0)


def use_proc_files():
    """
    Cause stdout/err from each MPI process to be written to [rank].out.
    """
    if MPI is not None:
        working_dir = os.environ.get('PROC_FILES_DIR')
        if not working_dir:
            ofile = open("%d.out" % MPI.COMM_WORLD.rank, 'wb')
        else:
            if not os.path.isdir(working_dir):
                raise RuntimeError("directory '%s' does not exist." % working_dir)
            ofile = open(os.path.join(working_dir, "%d.out" % MPI.COMM_WORLD.rank), 'wb')
        _redirect_streams(ofile.fileno())


def under_mpirun():
    """
    Return True if we're being executed under mpirun.

    Returns
    -------
    bool
        True if the current process is executing under mpirun.
    """
    # this is a bit of a hack, but there appears to be
    # no consistent set of environment vars between MPI
    # implementations.
    for name in os.environ.keys():
        if name == 'OMPI_COMM_WORLD_RANK' or \
           name == 'MPIEXEC_HOSTNAME' or \
           name.startswith('MPIR_') or \
           name.startswith('MPICH_'):
            return True
    return False


if under_mpirun():
    from mpi4py import MPI

    def debug(*msg):  # pragma: no cover
        """
        Print debug message to stdout.

        Parameters
        ----------
        *msg : tuple of str
            Strings to be printed.
        """
        newmsg = ["%d: " % MPI.COMM_WORLD.rank] + list(msg)
        for m in newmsg:
            sys.stdout.write("%s " % m)
        sys.stdout.write('\n')
        sys.stdout.flush()
else:
    MPI = None

    def debug(*msg):  # pragma: no cover
        """
        Print debug message to stdout.

        Parameters
        ----------
        *msg : tuple of str
            Strings to be printed.
        """
        for m in msg:
            sys.stdout.write("%s " % str(m))
        sys.stdout.write('\n')


class FakeComm(object):
    """
    Fake MPI communicator class used if mpi4py is not installed.

    Attributes
    ----------
    rank : int
        index of current proc; value is 0 because there is only 1 proc.
    size : int
        number of procs in the comm; value is 1 since MPI is not available.
    """

    def __init__(self):
        """
        Initialize attributes.
        """
        self.rank = 0
        self.size = 1


@contextmanager
def multi_proc_fail_check(comm):
    """
    Raise an AnalysisError on all procs if it is raised on one.

    Wrap this around code that you want to globally fail if it fails
    on any MPI process in comm.  If not running under MPI, don't
    handle any exceptions.

    Parameters
    ----------
    comm : MPI communicator or None
        Communicator from the ParallelGroup that owns the calling solver.
    """
    if MPI is None:
        yield
    else:
        try:
            yield
        except AnalysisError:
            msg = traceback.format_exc()
        else:
            msg = ''

        fails = comm.allgather(msg)

        for i, f in enumerate(fails):
            if f:
                raise AnalysisError("AnalysisError raised in rank %d: traceback follows\n%s"
                                    % (i, f))


@contextmanager
def multi_proc_exception_check(comm):
    """
    Raise an exception on all procs if it is raised on one.

    Wrap this around code that you want to globally fail if it fails
    on any MPI process in comm.  If not running under MPI, don't
    handle any exceptions.

    Parameters
    ----------
    comm : MPI communicator or None
        Communicator from the ParallelGroup that owns the calling solver.
    """
    if MPI is None:
        yield
    else:
        try:
            yield
        except Exception:
            msg = traceback.format_exc()
        else:
            msg = ''

        fails = comm.allgather(msg)

        for i, f in enumerate(fails):
            if f:
                raise RuntimeError("Exception raised in rank %d: traceback follows\n%s"
                                   % (i, f))


if MPI:
    def mpirun_tests():
        """
        Run individual tests under MPI.

        This is used in the "if __name__ == '__main__'" block to run an
        individual test in the file under MPI.  Note that if the test
        file has not been run under mpirun, this reverts to running
        unittest.main().
        """
        mod = __import__('__main__')

        tests = [arg for arg in sys.argv[1:] if not arg.startswith('-')]

        if tests:
            for test in tests:
                parts = test.split('.', 1)
                if len(parts) == 2:
                    tcase_name, method_name = parts
                    testcase = getattr(mod, tcase_name)(methodName=method_name)
                    setup = getattr(testcase, 'setUp', None)
                    if setup is not None:
                        setup()
                    getattr(testcase, method_name)()
                    teardown = getattr(testcase, 'tearDown', None)
                    if teardown:
                        teardown()
                else:
                    funcname = parts[0]
                    getattr(mod, funcname)()
        else:
            unittest.main()
else:
    mpirun_tests = unittest.main


if os.environ.get('USE_PROC_FILES') or os.environ.get('PROC_FILES_DIR'):
    use_proc_files()
