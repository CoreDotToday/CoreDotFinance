.. currentmodule:: coredotfinance

CoreDotFinance
===============
Version : 0.0.1

:mod:`CoreDotFinance` is financial data library, easy-to-get financial data from
**KRX** for Korean Stock price data  and **Binance** for Cryptocurrency.

**Core.Today**: `https://core.today <https://core.today>`__

**KRX**: `https://data.krx.co.kr <https://data.krx.co.kr>`__

**Binance** `https://binance.com <https://binance.com>`__


Quick Start
-----------

Install using ``pip``

.. code-block:: shell

   pip install coredotfinance

and then import and use one of data-getting function.
This example reads two months of price data on Samsung.

.. code-block:: python

   import coredotfinance.krx as krx
   # code number '005930' stands for Samsung
   krx.get('005930')


This example reads 500 rows of Bitcoin price data

.. code-block:: python

   import coredotfinance.crypto as coin
   # ticker 'BTCUSDT' stands for Bitcoin
   coin.get_ohlcv('BTCUSDT')

Contents
--------
.. panels::
   :card: + intro-card text-center

   ---
   :img-top: _static/krx.png

   **KRX**

   Do you want to get financial data from *KRX*? Check out the *KRX* guides.
   It will allow you to have  a lot of easy-to-use financial data.
   coming from `data.krx.co.kr <https://data.krx.co.kr>`__

   +++

   .. link-button:: krx
            :type: ref
            :text: To KRX guides
            :classes: bot-block btn-outline-primary

   ---
   :img-top: _static/binance.svg

   **Crypto Currency**


   Crypto Currency! The rising star in financial market.
   CoreDotFinance brings price data of cypto currency from `binance.com <https://www.binance.com>`__

   +++

   .. link-button:: crypto
            :type: ref
            :text: To binance guides
            :classes: bot-block btn-outline-primary


.. toctree::
   :maxdepth: 1

Recent developments
-------------------
You can install the latest development version using

.. code-block:: shell

   pip install git+https://github.com/CoreDotToday/CoreDotFinance.git

or

.. code-block:: shell

   git clone https://github.com/CoreDotToday/CoreDotFinance.git
   cd CoreDotToday
   python setup.py install


Examples
--------

refer to Examples

.. toctree::
   :maxdepth: 1

   examples.rst


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 1

   krx.rst
   crypto.rst