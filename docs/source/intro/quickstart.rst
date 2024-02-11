==========
Quickstart
==========

Pyttman ships with a CLI tool which is available after pip install.
It helps creating and running your apps with simple commands.

.. code-block:: console

    # Install it
    pip install pyttman

    # Create an app from a template
    pyttman new app my_first_app

    # Create an Ability module with files from a template
    pyttman new ability ability_name my_first_app

    # Run it in dev mode
    pyttman dev my_first_app

    # Run it in shell mode, and interact with your objects through a console with Pyttman 
    modules and objects loaded
    pyttman shell my_first_app

    # Run it in production mode, for your platform of choice as set in settings.py
    pyttman runclient my_first_app