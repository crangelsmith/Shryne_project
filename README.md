### Shryne project

Authors: Camila Rangel Smith, Alexander Green, Daniel Fisher and Sophie Cowie

Building analytic tools which can analyze a users relationships based on data such as email, text, facebook and whatsapp messages.

The structure of this repo is based on [this 
article](https://ldocao.wordpress.com/2015/11/06/optimize-the-code-structure-of-a-data-science-project/).

A reminder for what we should store, and where: 

- **setup**: you can define here all path, filenames etc
- **mining**: scripts to gather your data (eg: crawling), this should be fairly small (say a couple of files). If not, it means it’s a 
whole 
project by itself, and should be move out into a separate repo.
- **data**: the data you will analyze (eg: all the name of your clients who had an affair). Let me emphasize that your data should be in 
read-only mode. If it’s a constantly updated data, it means you should use a database or something more robust than your hard drive to store 
your data. In this case, you would put here a link to your database.
- **cleaning**: everything you need to do because someone else hasn’t done his job (features engineering included). Due to the lego 
principle, 
you might want to write a separate function in which you just call a series of functions to apply all the cleaning to you data.
- **analytics**: the fancy machine learning algorithm that you will use
- **out**: any temporary files that you want to create (eg: to save time, or give to someone else)
- **figures**: all plots and visualisations


Also bear in mind: Everything which is in analytics do not “see” the functions inside cleaning for example. This is a problem because most 
likely, you want to apply first your cleaning scripts before analyzing them. This is why the setup directory exists. You need then to 
proceed in 3 steps:

- define the path to the root of your repo
- copy setup_dir.py in each of your subfolders in cleaning and/or analytics
- from setup_dir import * at the top of each of your script

If you strictly follow the aforementioned structure, then you can then just do: import `my_script` wherever is `my_script.py`, and wherever 
you are calling this module from.