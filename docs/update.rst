Updating LISA
=============

Once LISA has been successfully installed on your computer, simply follow below
steps to update.

In the root folder of LISA ``(...\lisa\)``, run

.. code:: bash

    git pull

to keep your local source code in sync with the latest code in repo, and then
run

.. code:: bash

    poetry install -E "azure libvirt"

to keep all packages up-to-date as well.
