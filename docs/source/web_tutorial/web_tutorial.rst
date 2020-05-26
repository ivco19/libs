Web Tutorial
============

Arcovid19 viene acompañado de una utilidad para la vizualización
online de modelos epidemidologicos.

La forma mas simple de lanzar esta aplicación es simplemente
ejecutar

.. warning::

    Esto es un servidor de prueba, y no debe ser utilizado en un ambiente
    de producción por ningun motivo.

.. code-block:: console

    $ arcovid19 webserver
    * Serving Flask app "arcovid19.web" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with inotify reloader
    * Debugger is active!
    * Debugger PIN: XXX

Esto lanza una aplicación **local** la cual puede accederse a a traves de la url ``http://localhost:5000``.


.. figure:: images/landing.png
    :width: 100%

    Default view of arcovid19 webclient in version 0.5.

Si por algún motivo es necesario lanzar la app en otro *IP* o *port*, esto puede especificarse con las opciones
``--host`` y ``--port`` respectivamente. Por ejemplo si se desea servir para la red local en el puerto *8000* el comando seria:

.. code-block:: console

    $ arcovid19 webserver --host 0.0.0.0 --port 8000
    * Serving Flask app "arcovid19.web" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
    * Restarting with inotify reloader
    * Debugger is active!
    * Debugger PIN: 242-079-243

Esto permitiria a cualquier persona conectada a la misma red local que la computadora donde se lanza la webapp, pueda acceder a la pagina web a traves de la IP del servidor y el puerto *8000*

.. note::

    Para mas opciones de webserver puede ejecutar el comando
    ``arcovid19 webserver --help``.


Cambiando de idioma
-------------------

Hasta el momento arcovid19 web solo tiene dos idiomas implementados.

#. ``en`` - Ingles (Activado por defecto)
#. ``es`` - Español.

Para activar el idioma alternativo debe asiganrse una
`variable de entorno <https://en.wikipedia.org/wiki/Environment_variable>`_.
llamada ``ARCOVID19_DEFAULT_LOCALE``.

Esto se realiza con el comando

.. code-block:: console

    $ export ARCOVID19_DEFAULT_LOCALE=es;

Luego de esto simplemente es cuestion de lanzar la aplicacion con
``arcovid19 werbserver``.


Deployment
----------

Para ejecutando arcovid19 webserver en un entorno de producción debe configurarse almenos 2 variables de entorno:

- ``ARCOVID19_DEBUG=false``
- ``ARCOVID19_SECRET_KEY=a-lot-of-random-chars``

*ARCOVID19_SECRET_KEY* tiene que ser un string al azar contiguo de valores aleatorios,
puede por ejemplo apretarse teclas sin ningun sentido.

Si se desea configurar el idioma a español debe exportarse la variable de entorno

- ``ARCOVID19_DEFAULT_LOCALE=es``

El deployment puede realizarse con cualquier método disponible para
`Flask <https://flask.palletsprojects.com/en/1.1.x/deploying/>`_, y la
aplicacion wsgi esta disponible con la función ``arcovid19.web.create_app()``.

Por ejemplo para lanzar la applicación con `Gunicorn <https://gunicorn.org/>`_
puede hacerse con el comando

.. code-block:: console

    $ gunicorn 'arcovid19.web:create_app()'


Ademas el repositorio ya se encuentra configurado con los archivos
*requirements.txt* y *Procfile* para funcionar en `Heroku <http://heroku.com>`_.

Una versión online de la webapp esta disponible en
`aquí <https://arcovid19.herokuapp.com/>`_.






