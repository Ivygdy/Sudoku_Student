import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def forwardChecking ( self ):
        # Constraint Propagation
        mVars = set()
        for c in self.network.getModifiedConstraints():
            for v in c.vars:
                mVars.add(v)

        for v in mVars:
            if v.getDomain().isEmpty():
                return False
            for n in self.network.getNeighborsOfVariable(v):
                if v.getAssignment() in n.getValues():
                    if not n.isAssigned():
                        self.trail.push(n)
                        n.removeValueFromDomain(v.getAssignment())
                    else:
                        return False
            # Check the consistency
            for c in self.network.getConstraintsContainingVariable(v):
                if not c.isConsistent():
                    return False
        return True
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def norvigCheck ( self ):
        # If a variable is assigned then eliminate that value from the square's neighbors
        if not self.forwardChecking():
            return False

        # If a constraint has only one possible place for a value then put the value there.

        for c in self.network.getConstraints(): 
            n = [0] * self.gameboard.N
            for i in range(self.gameboard.N):
                for val in c.vars[i].getValues():
                    n[val-1] += 1
            for i in range(self.gameboard.N):
                if n[i] == 1:
                    for var in c.vars:
                        if var.getDomain().contains(i+1):
                            self.trail.push(var)
                            var.assignValue(i+1)
            
        return self.assignmentsCheck()
    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
       
        # If a variable is assigned then eliminate that value from the square's neighbors
        if not self.forwardChecking():
            return False

        # If a constraint has only one possible place for a value then put the value there.

        for c in self.network.getConstraints(): 
            n = [0] * self.gameboard.N
            for i in range(self.gameboard.N):
                for val in c.vars[i].getValues():
                    n[val-1] += 1
            for i in range(self.gameboard.N):
                if n[i] == 1:
                    for var in c.vars:
                        if var.getDomain().contains(i+1):
                            self.trail.push(var)
                            var.assignValue(i+1)
            
        return self.assignmentsCheck()
    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        temp = {}
        for var in self.network.getVariables():
            if not var.isAssigned():
                temp[var] = var.domain.size()
        res = sorted(temp.items(),key=lambda x:x[1])
        if len(res) > 0:
            return res[0][0]
        else:
            return None
        

    """
        Part 2 TODO: Implement the Degree Heuristic

        Return: The unassigned variable with the most unassigned neighbors
    """
    def getDegree ( self ):
        localMax = 0
        varMaxDegree = None
        for v in self.network.variables:
            if not v.isAssigned():
                degreeCount = 0                
                for n in self.network.getNeighborsOfVariable(v):
                    if not n.isAssigned():
                        degreeCount += 1
                if degreeCount > localMax:
                    localMax = degreeCount
                    varMaxDegree = v
        return varMaxDegree
    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with, first, the smallest domain
                and, second, the most unassigned neighbors
    """
    def MRVwithTieBreaker ( self ):
        mini = 1000000
        mrvtie = []
        order = {}
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() < mini:
                    mrvtie.append(v)
                    mini = v.domain.size()
                elif v.domain.size() == mini:
                    mrvtie.append(v)
        if len(mrvtie)  == 0:
            return None
        elif len(mrvtie)  == 1:
            return mrvtie[0]
        else:
            for v in mrvtie:
                count = 0
                for n in self.network.getNeighborsOfVariable(v):
                    if (not n.isAssigned()):
                        count += 1
                        order[v] = count
            res = sorted(order.items(), key=lambda x: x[1], reverse=True)
            mrvtie = [k for k,v in res]
            return mrvtie[0]

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):

        mini = 1000000
        mrvtie = []
        order = {}
        for v in self.network.variables:
            if not v.isAssigned():
                if v.domain.size() < mini:
                    mrvtie.append(v)
                    mini = v.domain.size()
                elif v.domain.size() == mini:
                    mrvtie.append(v)
        if len(mrvtie)  == 0:
            return None
        elif len(mrvtie)  == 1:
            return mrvtie[0]
        else:
            for v in mrvtie:
                count = 0
                for n in self.network.getNeighborsOfVariable(v):
                    if (not n.isAssigned()):
                        count += 1
                        order[v] = count
            res = sorted(order.items(), key=lambda x: x[1], reverse=True)
            mrvtie = [k for k,v in res]

            return mrvtie[0]
    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        temp = {}
        l = []
        for value in v.domain.values:
            constraintCount = 0
            for var in self.network.getNeighborsOfVariable(v):
                if value in var.getValues():
                    constraintCount += 1
                temp[value] =  constraintCount
        res = sorted(temp.items(), key = lambda x:x[1])
        for (key, val) in res:
            l.append(key)
        return l
    """
         OptionaleTODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        temp = {}
        l = []
        for value in v.domain.values:
            constraintCount = 0
            for var in self.network.getNeighborsOfVariable(v):
                if value in var.getValues():
                    constraintCount +=1
            temp[value] = constraintCount
        res = sorted(temp.items(),key=lambda x:x[1])
        for (key,val) in res:
            l.append(key)
        return l
    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "Degree":
            return self.getDegree()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
