# Programming Styles -- WiSe 20-21
---------

# Exercise 02

Implement the Word Index program using the **Monolithic Style**, **Cookbook Style** and the **Pipeline Style**.

The description of Word Index is the usual one:

Word Index is a program that takes a plain text file as input and outputs all the words contained in it sorted alphabetically along with the page numbers on which they occur. The program assumes that a page is a sequence of 45 lines. 
Each line has max 80 characters, and words cannot be split. Assume that no word is longer than 80 characters.


## Task 1: The Monolithic Style
To complete this task you must:

1. Implement the Word Index program using the **Monolithic Style** 
2. Implement at least three new tests in Python that make use of *temporary files*. Check that after the test execution the temporary files are automatically removed.

> NOTE: The Monolithic style in general forbids the use of high-level abstractions, such as classes, methods, modules, and functions. However, you can still use variables, loops, and the like.


## Task 2: The Cookbook Style

To complete this task you must:

1. Implement the Word Index program using the **Cookbook Style**

> NOTE: Make sure that you functions do not return values. You cannot use function composition and objects.

## Task 3: The Pipeline Style

To complete this task you must:

1. Implement the Word Index program using the **Pipeline Style** 
2. Implement at least one test for each function that is used inside the pipeline. Tests must make use of *mocks* to break dependencies.

> Note: Make sure that your functions always return a value. You cannot use global variables. Take special care of global constants.