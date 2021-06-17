.. _examples:

.. currentmodule:: coredotfinance

.. ipython:: python

   :suppress:

   import pandas as pd

   import numpy as np
   np.set_printoptions(precision=4, suppress=True)

   pd.options.display.max_rows=15


******************
Examples
******************

.. _examples.data_reader:

Functions from :mod:`coredotfinance.krx` and :mod:`coredotfinance.crypto`
extract data from various Internet sources into a pandas DataFrame.

    - :ref:`Krx<examples.krx>`
    - :ref:`Crypto<examples.crypto>`

.. _examples.krx:

Krx
======

This function without any arguments returns info of stocks listed on Korea stock market in the day.

Documentation :

.. toctree::
   :maxdepth: 1

   krx.rst

.. code-block:: ipython

   In [1]: import coredotfinance.krx as krx

   In [2]: df = krx.get()
   In [3]: df.head()

      종목코드     종목명    시장구분    소속부     종가   대비   등락률     시가     고가     저가     거래량      거래대금        시가총액        상장주식수
   0  060310      3S  KOSDAQ  중견기업부   3160      10   0.32    3130    3180    3085   322944    1.01241e+09  1.46218e+11  4.62715e+07
   1  095570  AJ네트웍스   KOSPI          5710     -70  -1.21    5780    5950    5710   116831    6.76312e+08  2.67355e+11  4.68223e+07
   2  006840   AK홀딩스   KOSPI         34000        0     0    34000   34300   33550   50160    1.69498e+09  4.50417e+11  1.32476e+07
   3  054620  APS홀딩스  KOSDAQ  중견기업부  14950    -50  -0.33   15000   15000   14600   73988    1.09317e+09  3.04894e+11  2.03942e+07
   4  265520   AP시스템  KOSDAQ  우량기업부  29750   -150   -0.5   29750   30050   29500  158057    4.69988e+09  4.30787e+11  1.44802e+07

With proper arguments about specific date and stock name or code, this function returns price data for the stock.

.. code-block:: ipython

   In [1]: import coredotfinance.krx as krx

   In [2]: krx.get('005930' , start=20210601, end=20210607)

                 종가      대비   등락률    시가      고가       저가       거래량        거래대금         시가총액         상장주식수    종목명
   2021-06-07  81900.0  -300.0 -0.36  82700.0  82800.0  81600.0  16496197.0  1.353521e+12  4.889252e+14  5.969783e+09  삼성전자
   2021-06-04  82200.0  -600.0 -0.72  82700.0  82700.0  81500.0  18112259.0  1.487791e+12  4.907161e+14  5.969783e+09  삼성전자
   2021-06-03  82800.0  2000.0  2.48  81300.0  83000.0  81100.0  29546007.0  2.438123e+12  4.942980e+14  5.969783e+09  삼성전자
   2021-06-02  80800.0   200.0  0.25  80400.0  81400.0  80300.0  16414644.0  1.327714e+12  4.823584e+14  5.969783e+09  삼성전자
   2021-06-01  80600.0   100.0  0.12  80500.0  81300.0  80100.0  14058401.0  1.135462e+12  4.811645e+14  5.969783e+09  삼성전자

This function also understands stock name as well.

.. code-block:: ipython

   In [1]: import coredotfinance.krx as krx

   In [2]: krx.get('005930' , start=20210601, end=20210607)

                 종가      대비   등락률    시가      고가       저가       거래량        거래대금         시가총액         상장주식수    종목명
   2021-06-07  81900.0  -300.0 -0.36  82700.0  82800.0  81600.0  16496197.0  1.353521e+12  4.889252e+14  5.969783e+09  삼성전자
   2021-06-04  82200.0  -600.0 -0.72  82700.0  82700.0  81500.0  18112259.0  1.487791e+12  4.907161e+14  5.969783e+09  삼성전자
   2021-06-03  82800.0  2000.0  2.48  81300.0  83000.0  81100.0  29546007.0  2.438123e+12  4.942980e+14  5.969783e+09  삼성전자
   2021-06-02  80800.0   200.0  0.25  80400.0  81400.0  80300.0  16414644.0  1.327714e+12  4.823584e+14  5.969783e+09  삼성전자
   2021-06-01  80600.0   100.0  0.12  80500.0  81300.0  80100.0  14058401.0  1.135462e+12  4.811645e+14  5.969783e+09  삼성전자

.. warning:: Stock name could be changed but not stock code. Using code is highly recommended

.. _examples.crypto:

crypto
=======

This function without any arguments returns price data of Bitcoin as a default.

.. code-block:: ipython

   In [1]: import coredotfinance.crypto as crypto

   In [2]: df = crypto.get_ohlcv()
   BTCUSDT
   In [3]: df.head()
                  시가               고가              저가              종가            거래량
   일시
   2021-06-16  40143.80000000  40527.14000000  38877.46000000  38955.52000000   38246.244675
   2021-06-15  40516.28000000  41330.00000000  39506.40000000  40144.04000000   80679.622838
   2021-06-14  39020.56000000  41064.05000000  38730.00000000  40516.29000000  108522.391949
   2021-06-13  35546.12000000  39380.00000000  34757.00000000  39020.57000000   86921.025555
   2021-06-12  37331.98000000  37463.63000000  34600.36000000  35546.11000000   87717.549990

With argument of sympol which stands for specific crypto currency, this function returns price data of the crypto currency.

.. code-block:: ipython

   In [1]: import coredotfinance.crypto as crypto

   In [2]: df = crypto.get_olhcv('ETHBTC')
   ETHBTC
   In [3]: df.head()
                  시가          고가          저가          종가         거래량
   일시
   2021-06-17  0.06175600  0.06241600  0.06163200  0.06210300    3322.111
   2021-06-16  0.06335500  0.06339700  0.06142500  0.06176100  120161.524
   2021-06-15  0.06370400  0.06520000  0.06296700  0.06334900  149346.695
   2021-06-14  0.06430600  0.06464600  0.06238900  0.06369900  163306.557
   2021-06-13  0.06669200  0.06759900  0.06354000  0.06430600  142796.288

Documentation :

.. toctree::
   :maxdepth: 1

   crypto.rst
