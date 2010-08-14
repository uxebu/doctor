How to get Sphinx running locally
=================================

Setting up user documentation based in restructured text is very simple using the
doctor infrastructure.

NOTE
----

If doctor and your doc tools are already installed, simply run following command
to build your docs

$ sphinx-build -b html your/doc/source/ your/doc/dist/

1. Install Sphinx
-----------------

You need to have Sphinx installed on your machine to be able to generate docs.
Visit following link for installation instructions

http://sphinx.pocoo.org/

2. Create your project structure
--------------------------------

You are free to setup your project structure as you like though we suggest following.

/libs

The libs folder contains external libraries such as the doctor project.

/libs/doctor

/docs

The docs folder contains both user and api docs

/docs/user

3. Check out the doctor source tp your libs folder
--------------------------------------------------

$ git clone https://uxebu@github.com/uxebu/doctor.git /libs/doctor

Make sure to adjust the path accordingly

4. Initialize submodules
------------------------

$ cd /libs/doctor
$ git submodule init
$ git submodule update

5. Create documentation project
-------------------------------

$ cd /docs/user
$ sphinx-quickstart

Make sure following questions are answered as stated:

> Root path for the documentation [.]: .
> Create Makefile? (Y/n) [y]: n
> Create Windows command file? (Y/n) [y]: n

6. Adjust conf.py to use doctor settings
----------------------------------------

Open conf.py in the /docs/user directory and adjust the following properties:

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "libs", "doctor", "sphinx", "libs", "extensions"))

And

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ["../../libs/doctor/sphinx/libs/themes"]

And

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'uxebu'

And

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['uxebudocs']

7. Now build the docs from your docs directory with following command

$ sphinx-build -b html user/ dist/