#!/usr/bin/env python
import sys,  inspect, time

#
# The Aspects Style Description:
#
# - The problem is decomposed using some form of abstraction
#   (procedures, functions, objects, etc.)
#
# - Aspects of the problem are added to the main program without any
#   edits to the source code of the abstractions. These side functions
#   latch on the main abstractions by naming them, as in "I'm an aspect
#   of foo (even though foo may not know it!)"
#
#


# Import the pipeline implementation of Word Index
import pipeline_word_index as pipeline

# Global variables used by the aspects to store execution data
execution_times = {}
parameters      = {}

def profile_execution_time(f):
    """
        Wrap a function 'f' so we can profile its execution time
    """

    print("DEBUG: INSTRUMENTING FUNCTION ", f.__name__, "TO CAPTURE LOG EXECUTION TIME")

    def profilewrapper(*arg, **kw):


        # Store this in our global function
        global execution_times

        # Before Advice
        start_time = time.time()

        # Original Invocation
        ret_value = f(*arg, **kw)

        # After Advice
        elapsed = time.time() - start_time

        # Since we do not know how many times this function will be called we store the data into a list.
        # We assume that each function has a different name
        if f.__name__ not in execution_times:
            execution_times[f.__name__] = []

        execution_times[f.__name__].append(elapsed)

        # Return the ORIGINAL value
        return ret_value

    # Return the profiled function object
    return profilewrapper


def profile_parameters(f):
    """
        Wrap the function 'f' to capture information about its parameters
    """

    print("DEBUG: INSTRUMENTING FUNCTION ", f.__name__, "TO CAPTURE PARAMETERS")

    def profilewrapper(*arg, **kw):

        # Store the data in the global variable
        global parameters

        # Before Advice. Collect info on the parameters: formal name, actual type or None, str()
        if f.__name__ not in parameters:
            parameters[f.__name__] = []

        meta = {}

        # arg and kw give us the reference to the arguments if any, but not their definition, so no name and type
        # We could use locals(); however, since here we are not inside the function 'f', local()
        # will give us the local table of this profilewrapper function. So we need to use introspection on 'f'.
        # First we get the number of parameters, N, and take the FIRST N elements of the varnames

        for i in range(f.__code__.co_argcount):
            arg_name =  f.__code__.co_varnames[i]
            arg_type = type(arg[i]).__name__ if arg[i] is not None else "None"
            # take the string value but limit it to the first 10 chars ...
            arg_value = str(arg[i])[0:10] if arg[i] is not None else ""

            meta["name"] = arg_name
            meta["type"] = arg_type
            meta["str_value"] = arg_value

        parameters[f.__name__].append(meta)

        # Original Invocation
        ret_value = f(*arg, **kw)

        # After Advice: Do nothing

        # Return the ORIGINAL value
        return ret_value

    return profilewrapper


def main(file_path):

    # Join points are all methods in the pipeline.
    # So we do not really need the names of the functions as we see in the book.
    # It would get all the functions defined in the pipeline... well, except main
    join_points = [o[1] for o in inspect.getmembers(pipeline) if
                   inspect.isfunction(o[1]) and
                   inspect.getmodule(o[1]) == pipeline and
                   o[1].__name__ != "main"]

    # Do the Weaving. Note that we cannot use globals() as that refers to "this" module global symbol table
    # See https://stackoverflow.com/questions/29054442/wrapping-a-function-imported-with-import for more details
    for target_function in join_points:
        f1 = profile_parameters(target_function)
        f1.__name__ = target_function.__name__

        f2 = profile_execution_time(f1)
        f2.__name__ = target_function.__name__

        setattr(pipeline, target_function.__name__, f2)

        # Q: This won't work... why?
        # setattr(pipeline, target_function.__name__, profile_execution_time(target_function))
        # setattr(pipeline, target_function.__name__, profile_parameters(target_function))

        # Q: This won't work... why?
        # setattr(pipeline, target_function.__name__, profile_execution_time(profile_parameters(target_function)))

    # Invoke the pipeline main
    pipeline.main(file_path)

    # Print out the summary of execution by iterating at once over both dictionaries
    # print("Summary on Parameters:")
    # for r in [(k, v) for k, v in parameters.items()]:
    #     print(r)
    #
    # print("Summary on Executiong times:")
    # for r in [(k, v) for k, v in execution_times.items()]:
    #     print(r)
    #

    print("Summary:")
    for r in [(k, v, parameters[k]) for k, v in execution_times.items()]:
        print(r)


if __name__ == "__main__":
    main(sys.argv[1])