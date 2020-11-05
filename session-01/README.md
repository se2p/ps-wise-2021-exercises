# Programming Styles -- WiSe 20-21
---

# Exercise 01

## Task 1: Setup
During this class, we will use Python (v3.7), Java (JDK11) and JavaScript (NodeJS v10.23). The first task consists in:

1. Installing the required versions of Python, Java and JavaScript.
2. Implementing a simple "Hello world" program in all the languages.
3. Executing all the programs and checking that they work correctly

Please follow the installation instructions listed in the [instructions file](./instructions.md).

> **NOTE**: The installation instructions describe only some of the possible ways to install the required software, hence they are incomplete. If you find better, simpler, or different ways to install the required software contribute to them to the repository.

Inside the `task-01` folder you find the empty files `HelloWorld.java`, `hello-world.js`, and `hello-world.py` to fill.

## Task 2: Free Flow - Python
Implement the Word Index program without using any style (**Free Flow**).

Word Index is a program that takes a plain text file as input and outputs all the words contained in it sorted alphabetically along with the page numbers on which they occur. The program assumes that a page is a sequence of 45 lines. 
Each line has max 80 characters, and words cannot be split. Assume that no word is longer than 80 characters.

Additionally, Word Index must ignore all words that occur more than 100 times.

To complete this task you must use Python to implement Word Index and three unit tests using the[`unittest`](https://docs.python.org/3/library/unittest.html) library.

Inside the `task-02` folder, you find the empty file `word_index.py` that you have to fill and a sample unit test `word_index_unit_tests.py`.


## Task 3: Free Flow - Java

Re-implement the Word Index program without using any style (**Free Flow**), but use Java this time. As before, implement three unit tests using [`JUnit4`](https://junit.org/junit4/) and [`Hamcrest`](http://hamcrest.org/)

Inside the `task-03` folder, you find the empty file `WordIndex.java` that you have to fill and a sample JUnit Test Case  `WordIndexTest.java`.

> **BONUS**: Implement a simple `makefile` to build the program and test it.

## Task 4: Free Flow - Java

Re-implement the Word Index program without using any style (**Free Flow**), but use Javascript this time. As before, implement three unit tests using [`mocha`](https://mochajs.org/).

Inside the `task-04` folder, you find the empty file `word-index.js` that you have to fill and a sample mocha unit tests  `test/basic-test.js`.

> **BONUS**: Implement a simple `makefile` to build the program and test it.