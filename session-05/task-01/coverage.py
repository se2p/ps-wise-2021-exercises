#!/usr/bin/env python

import sys
import inspect

from importlib.machinery import SourceFileLoader

#
# The Introspective Style Description:
#
# - The problem is decomposed using some form of 
#   abstraction (procedures, functions, objects, etc.)
# 
# - The abstractions have access to information about 
#   themselves, although they cannot modify that information
#
#
# The Reflective Style Description:
# - The problem is decomposed using some form of 
#   abstraction (procedures, functions, objects, etc.)
# 
# - The abstractions have access to information about 
#   themselves, although they cannot modify that information
#


class Coverage:
    """
        This class implements a python ContextManager so it will automatically turned on and off at runtime.
        To measure METHOD coverage we implement the approach described by Prof. A. Zeller in his book [1].

        [1] https://www.fuzzingbook.org/html/Coverage.html
    """

    def __init__(self, imported_module):

        self._imported_module = imported_module

        # Compute basic properties of the imported_module using introspection

        # Gather data about 'global' functions in the target module
        list_of_functions = [o[0] for o in inspect.getmembers(self._imported_module)
                                  if inspect.isfunction(o[1]) and inspect.getmodule(o[1]) == self._imported_module]

        # Gather data about classes and methods in the target module.
        list_of_methods = []
        for class_name, class_obj in inspect.getmembers(self._imported_module, predicate=inspect.isclass):
            for member_name, member_obj in inspect.getmembers(class_obj):
                # Q: For some reason methods are not always tagged as such, any idea why?
                if (inspect.isfunction(member_obj) or inspect.ismethod(member_obj))\
                        and inspect.getmodule(member_obj) == self._imported_module:
                    # Store the "fully qualified name" of the method
                    fqn = ".".join([class_name, member_name])
                    list_of_methods.append(fqn)

        # Holds data about module's code
        self._function_coverage = dict.fromkeys(list_of_functions, 0)
        self._method_coverage = dict.fromkeys(list_of_methods, 0)

        # Holds execution trace
        self._trace = []

    def _get_class_from_frame(self, fr):
        """
            Utility method to retrieve the class object from the trace object. Since this is not trivial at all
            we assume the target program is written according to the "standard python style," so we check that
            the first parameter of instance methods is named 'self' to identify instance-level class methods.
        """
        args, _, _, value_dict = inspect.getargvalues(fr)

        # This will miss static methods
        if len(args) and args[0] == 'self':
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get('self', None)
            if instance:
                # return its class
                return getattr(instance, '__class__', None)
        # return None otherwise
        return None

    def traceit(self, frame, event, arg):
        """
            Tracing method invocation
        """

        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        # Extract data from execution
        function_name = frame.f_code.co_name
        lineno = frame.f_lineno
        # Utility method
        class_obj = self._get_class_from_frame(frame)

        # If you are curious to see the events that are generated during the execution
        #   you can print them. Note that since we work by introspection and reflection,
        #   using a debugger DOES NOT work here !
        # Q: Can you guess why?
        # print("TRACE", event, "->", frame.f_code.co_name, lineno, class_obj)

        if event == "call":
            self._trace.append((function_name, lineno))

            # Calls to static functions or functions that are not associated to any object
            if class_obj is None:
                if function_name in self._function_coverage.keys():
                    # Mark this function as covered
                    self._function_coverage[function_name] = 1
                return

            if class_obj is not None:
                class_name = class_obj.__name__
                fqn = ".".join([class_name, function_name])
                if fqn in self._method_coverage.keys():
                    self._method_coverage[fqn] = 1

        if event == "line":
            self._trace.append((function_name, lineno))

        # The trace function is invoked (with event set to 'call') whenever a new local scope is entered;
        # it should return a reference to a local trace function to be used that scope, or None if the scope
        # shouldn’t be traced."
        # Here it returns itself, to handle all the tracing in the same function.
        # A function is an object like anyone else, so there's no problem in returning itself.
        # For example, it allows repeated calling on the same line:
        #
        # traceit("abc", "def", None)("ghi", "jkl", 3)("mno", "pqr", 4.3)
        #
        return self.traceit

    # Start of `with` block
    def __enter__(self):
        """ Check https://www.geeksforgeeks.org/python-sys-settrace/"""
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

    def trace(self):
        """
            The list of executed lines, as (function_name, line_number) pairs
        """
        return self._trace

    def coverage(self):
        """
            The set of executed lines, as (function_name, line_number) pairs
        """
        return set(self.trace())

    def print_coverage_summary(self):
        """
            The set of executed lines, as (function_name, line_number) pairs
        """
        total_functions = len(self._function_coverage.keys())
        covered_functions = len([f for f in self._function_coverage.keys() if self._function_coverage[f] == 1])

        total_methods = len(self._method_coverage.keys())
        covered_methods = len([m for m in self._method_coverage.keys() if self._method_coverage[m] == 1])

        print("COVERAGE SUMMARY")
        if total_functions > 0:
            print()
            print("Covered", "".join([str((covered_functions/total_functions)*100), "%"]), "out of", total_functions, "functions")
            for name in self._function_coverage.keys():
                if self._function_coverage[name] == 1:
                    print("# ", end="")
                else:
                    print("  ", end="")
                print(name)
            print()

        if total_methods > 0:
            print()
            print("Covered", "".join([str((covered_methods / total_methods) * 100), "%"]), "out of", total_methods, "methods")
            for method_name in self._method_coverage.keys():
                if self._method_coverage[method_name] == 1:
                    print("# ", end="")
                else:
                    print("  ", end="")
                print(method_name)
            print()

    def annotated_code(self):
        # decode_code is a string holding the source code.
        # We can later print it out with Python syntax highlighting:
        decode_code = inspect.getsource(self._imported_module)
        decode_lines = [""] + decode_code.splitlines()
        covered_lines = [line[1] for line in self.coverage()]

        for lineno in range(1, len(decode_lines)):
            prefix ="  "
            if lineno in covered_lines:
                prefix = "* "

            decode_lines[lineno] = "".join([prefix, str(lineno).zfill(3), " ", decode_lines[lineno]])
        return decode_lines


def main(arguments):

    word_index = arguments[1]
    input_file = arguments[2]

    # Import the module given in input
    # Note: We work under the assumption that the module has a "main(args)" function
    imported_module = SourceFileLoader("module.name", word_index ).load_module()

    # Execute the main method in the module, and compute coverage. Method coverage
    #   data are stored inside the coverage object
    with Coverage(imported_module) as coverage:
        imported_module.main(input_file)

    # Plot coverage information:
    coverage.print_coverage_summary()

    # Print the content of source file indicating the covered elements
    # print("COVERED TARGETS:")
    # for line in coverage.annotated_code():
    #     print(line)


if __name__ == "__main__":
    main(sys.argv)