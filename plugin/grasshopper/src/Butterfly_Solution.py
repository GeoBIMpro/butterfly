# Butterfly: A Plugin for CFD Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Butterfly.
#
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Run recipes using OpenFOAM.

-

    Args:
        _recipe: A Butterfly recipe.
        _numOfCPUs_: number of cpus for parallel run.
        solutionParams_: Butterfly solutionParams. These parameters can be edited
            while the analysis is running.
        _interval_: Time interval for updating solution in Grasshopper in seconds.
            (default: 2 seconds)
        _write_: Write changes to folder.
        _run: start running the solution.
    Returns:
        readMe!: Reports, errors, warnings, etc.
        case: Butterfly case.
"""

ghenv.Component.Name = "Butterfly_Solution"
ghenv.Component.NickName = "solution"
ghenv.Component.Message = 'VER 0.0.01\nSEP_21_2016'
ghenv.Component.Category = "Butterfly"
ghenv.Component.SubCategory = "07::Solver"
ghenv.Component.AdditionalHelpFromDocStrings = "1"

from subprocess import Popen
import time
from scriptcontext import sticky

try:
    from butterfly.gh.timer import ghComponentTimer
    from butterfly.solution import Solution, SolutionParameters
except ImportError as e:
    msg = '\nFailed to import butterfly. Did you install butterfly on your machine?' + \
            '\nYou can download the installer file from github: ' + \
            'https://github.com/mostaphaRoudsari/Butterfly/tree/master/plugin/grasshopper/samplefiles' + \
            '\nOpen an issue on github if you think this is a bug:' + \
            ' https://github.com/mostaphaRoudsari/Butterfly/issues'
        
    raise ImportError('{}\n{}'.format(msg, e))

uniqueKey = str(ghenv.Component.InstanceGuid)

if _numOfCPUs_:
    raise NotImplementedError('NotImplemented > Parallel run will be implemented soon!')
if not _interval_:
    _interval_ = 2

if _recipe and _write: 
    try:
        if uniqueKey not in sticky:
            # solution hasn't been created or has been removed
            # create a new one and copy it to sticky
            solution = Solution(_recipe)
            
            solution.updateSolutionParams(solutionParams_)
            
            sticky[uniqueKey] = solution
            if run_:
                solution.run()
        else:
            # solution is there so just load it
            solution = sticky[uniqueKey]
    
        status = solution.isRunning
        
        if status:
            print 'running...'
            # update parameters if there has been changes.
            solution.updateSolutionParams(solutionParams_)
            ghComponentTimer(ghenv.Component, interval=_interval_*1000)
        else:
            # analysis is over
            print 'done!'
            solution = sticky[uniqueKey]
            # remove solution from sticky
            del(sticky[uniqueKey])
            
            # set run toggle to False
            
            
    except Exception as e:
        # clean up solution in case of failure
        if uniqueKey in sticky:
            del(sticky[uniqueKey])
        raise Exception(str(e))
        
    logFile = _recipe.logFile