[![Documentation Status](https://readthedocs.org/projects/interview-task/badge/?version=latest)](https://readthedocs.org/projects/interview-task/?badge=latest)
[![Build Status](https://travis-ci.org/inirudebwoy/interview-task.svg?branch=develop)](https://travis-ci.org/inirudebwoy/interview-task)

Overview
========

This test is designed to test your problem solving ability, your knowledge of Object Oriented programming and your understanding of the HTTP protocol. The aim is to assess your problem solving approach, your ability to turn your solution into working code and the way in which you structure your code.

Requirements
============

* The test does not have a time limit but the time it takes you to implement your solution will be taken into account during assessment.
* When the project has been completed it should be presented in a state that is maintainable by another developer.  To that end:
* Tell us how to run the app
  - Tell us how to run your tests
  - Tell us how to retrieve the data that the app stores
  - Don’t forget comments in any code that needs them!
* This project should be submitted as a github repository which should be committed to frequently
* You can use any operating system to host your environment but a development framework (e.g. Django) should not be used to complete the test (the test is trying assess a low level understanding of software development which use of a framework would mask).
* While use of frameworks is not permitted, standard/common libraries and modules (such as curl) may be used. Additionally you may use any reference material you desire in order to aid your development.
* You must create a command line script that is able to retrieve data from a web server, process that data and output the correct results to the console. The code should be written in such a way that all of the required test results could be obtained by passing in command line options to the script.
* The script will need to be able to handle errors gracefully and will need to implement some kind of caching/storage so that once executed successfully it could still be used should an Internet connection become unavailable.
* The script should be separated into separate modules that handle specific areas of functionality and should be structured in such a way as to allow for future extension or maintenance to be as easy as possible.
* All tests should be submitted to your test coordinator on the same day that they were issued.
* Once your test is completed you must email your test coordinator.

You will need a working development environment setup that includes:

* Internet access
* Python interpreter (as the solution should be written in Python as it our language of choice)

Problem
=======

The following website contains a list of all the birth names given to babies between 1880 and 2010, and provides options to select a birth year and number of results between the top 20 and top 1000 most popular given names each year.

http://www.socialsecurity.gov/OACT/babynames/

Your task will be to construct a command line script that returns the arithmetic mean of the rank of male children within the top 1000 results over a given period of time.

Specifically, provide results for the following names and date periods, where the years are inclusive:
* Billy between 1892 and 2001
* Jamie between 1901 and 1987
* Daniel between 1996 and 1999
* Neil between 1957 and 1983
* Jordan between 1880 and 2010

The script should accept a name and a start and end year as input parameters, e.g.

```shell
  ./scriptName [name] [start year] [end year]
  ./scriptName Billy 1892 2001
```

So expected behaviour might be:

```shell
  $ ./scriptName Michael 2004 2009
  Between 2004 and 2009 the average popularity rank of the name Michael was 2.17
```

The results obtained from running your script with the above input values should be included in your return email along with your code.

Tips
====

* The ability to view the contents of an outgoing HTTP request from a browser may help you to implement a solution. The Firebug plug­in for Firefox/Google Chrome has the ability to do this.
* It is more important to illustrate competency and quality than it is to complete the test in as short a time as possible.
* Focus on demonstrating best practice even if it would mean slightly over­engineering a script of this size.
* Don’t worry that the average rank won’t take into account different numbers of babies born in different years
* Also ­ we don’t make a habit of screen­scraping sites; it just makes an interesting test!
