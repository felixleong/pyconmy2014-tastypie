
.. Creating Powerful RESTful APIs with Django-Tastypie slides file, created by
   hieroglyph-quickstart on Fri Mar 14 15:11:09 2014.

Creating Powerful RESTful APIs with Django-Tastypie
===================================================

`Seh Hui Leong <http://twitter.com/felixleong/>`_ |br|
March 2014, Mini PyCon Malaysia 2014

.. figure:: /_static/4687542962_87bdc4f9f0_b.jpg
    :class: fill

    CC-BY-NC-SA https://flic.kr/p/89dTdf

.. ifnotslides::

    .. toctree::
        :maxdepth: 2

ACT 1: RESTful is AWESOME!
--------------------------

.. figure:: /_static/4960389917_1d0b48f117_b.jpg
    :class: fill

    CC http://www.flickr.com/photos/mccun934/4960389917/

REST-what?
__________

- REpresentational State Transfer
- **Paradigm/Infrastructure pattern to designing easy-to-understand APIs**
    - Both **machine- and programmer-readable** without convoluted protocols
- Usually called **RESTful** because no one seems to agree what a perfect REST
  service is

Making the Perfect Bread and Bacon
__________________________________

- Thinking in **resources**
- **Uniform Resource Identifier/Locator (URI/URL)**
- **HTTP**: The perfect **uniform interface**

HTTP: The Perfect Fit (I)
_________________________

You can represent CRUD actions using **HTTP verbs**

:**Create**: POST
:**Retrieve**: GET
:**Update**: UPDATE
:**Delete**: DELETE

HTTP: The Perfect Fit (II)
__________________________

You can get status of your requests using **HTTP status codes**

==== ================================
Code Meaning
==== ================================
200  OK
201  Created
204  No-Content (i.e. return void)
400  Bad Request
401  Unauthorized
403  Forbidden
404  Not Found
500  Internal Server Error (OMG BUG!)
==== ================================

HTTP: The Perfect Fit (III)
___________________________

You can use **HTTP headers** to specify operating parameters of a transaction.

============== ==========================
Request header Description
============== ==========================
Accept         Content we want to request
Authorization  Authentication credentials
============== ==========================

=============== =============================================
Response header Description
=============== =============================================
Status          Status of the transaction 
Location        The destination URI (important for redirects)
=============== =============================================

ACT 2: Hello World, Tastypie!
-----------------------------

.. figure:: /_static/3294261072_c635d74ce8_o.jpg
    :class: fill

    CC-BY-NC https://flic.kr/p/626X3G

ACT 3: Real World Tastypie Tips & Tricks
----------------------------------------

.. figure:: /_static/5650815548_59e3c82b6a_b.jpg
    :class: fill

    CC-BY-NC https://flic.kr/p/9BkUAh

FINALE: You Are Now Smarter!
----------------------------

.. figure:: /_static/6966069023_5512204921_b.jpg
    :class: fill

    CC-BY http://www.flickr.com/photos/sylvainkalache/6966069023/

You Have Learned…
_________________

- What is RESTful API?

GIMME EVERYTHING!
_________________

**Code, Demo, Presentation**

http://github.com/felixleong/pyconmy2014-tastypie/

:Email: felixleong@gmail.com
:Facebook: http://facebook.com/leongsh/
:Twitter: http://twitter.com/felixleong/

References
__________

- Tastypie
    - https://django-tastypie.readthedocs.org/en/latest/
- Tastypie-ExtendedModelResource
    - https://github.com/felixleong/django-tastypie-extendedmodelresource/
- My previous talk, RESTful API 101
    - https://github.com/felixleong/wckl_restapi_talk/
- REST in Practice, *by Jim, Savas and Ian* (O'Reilly)
    - http://shop.oreilly.com/product/9780596805838.do

License
_______

This work is licensed under a `Creative Commons Attribution-ShareAlike 3.0 Unported License`_.

.. _Creative Commons Attribution-ShareAlike 3.0 Unported License: http://creativecommons.org/licenses/by-sa/3.0/deed.en_US

.. CUSTOM DEFINITIONS

.. |br| raw:: html

    <br />
