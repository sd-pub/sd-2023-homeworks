# README check

## Description
This is the checker used to automatically grade the Virtual Memory Allocator. 

The name of the checker is `check`. It is written in `Python 3.6`.


## What does it do?
It will do the multiples steps.

All steps marked with `[STOP]` are required. If one failed the checker will stop.
All steps marked with `[OPTIONAL]` are optional and can be disabled from config.

1.  `deps`: Check if all dependencies are installed on local system in order to build/run/grade the homerwork.

2. `build`: Build homework.
	2.1. [STOP] `Makefile`: Check if `Makefile` exists.
	2.2. [STOP] `make`:  Run `make build` in order to build all binaries.
	2.3. [OPT]`warnings`:  If warnings are detected, a penalty to final grade is applied.

3. `run`: Run all tests for specified tasks (all or one).
	3.1 [STOP] `run`: Run task for current test. Continue iff the program exited successfully.
	3.2 [STOP] `check`: Check if the solution is correction. Continue iff the program found solution for task/at least one subtask.
	3.3 [OPT ] `valgrind`: Check for memory leaks and errors. If valgrind found problems, the test grade is 0.

	`Note`: This stage is using an explained `legend`:
	1. `UPS`: Ups, program crashed
		e.g null pointer dereference, negative or to big array/matrix indices
	2. `TLE`: Time Limit Exceed
		e.g. infinit loop or too slow
	3. `MLE`: Memory Limit Exceed
		e.g. too much allocated memory (in total or for some segments)
	3. `MEM_UPS`: Memory leaks or errors
		e.g. invalid memory access, unfreed dynamic-allocated arrays
	4. `WA`: Wrong Answer (wrong or partial output)
		e.g. output is missing or has other value
	5. `OK`: Everything is OK.

4. `style`: Run coding style checker to automatically report most common mistakes.

5. `README`: Basic check for reminding students to put a readme file before final submission.
  	`Note`: If the `README` is missing, a penalty to final grade is applied.

6. `clean`: Remove all generated files by running the `make clean` command.

7. `grade`: Print final grade (which is always non-negative).


## Installation

The `install.sh` script can be used to install all dependencies for `check`.

Note: Please inspect  the script to see which are the requirements.

```console
sudo ./install.sh
```

## Usage

- run entire homework

```console
./check
```

## Coding style checker

Please read `cs/README.md`.
