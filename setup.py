from setuptools import setup

setup(
    name='crawper',
    version='1.0',
    packages=['src', 'src.common', 'src.common.db', 'src.common.config', 'src.crawler', 'src.crawler.config',
              'src.crawler.threader', 'src.scraper', 'src.scraper.config', 'src.scraper.threader', 'src.r_engine',
              'src.r_engine.config', 'venv.lib.python2.7.distutils', 'venv.lib.python2.7.encodings',
              'venv.lib.python2.7.site-packages.bs4', 'venv.lib.python2.7.site-packages.bs4.tests',
              'venv.lib.python2.7.site-packages.bs4.builder', 'venv.lib.python2.7.site-packages.pip',
              'venv.lib.python2.7.site-packages.pip.req', 'venv.lib.python2.7.site-packages.pip.vcs',
              'venv.lib.python2.7.site-packages.pip.utils', 'venv.lib.python2.7.site-packages.pip.compat',
              'venv.lib.python2.7.site-packages.pip.models', 'venv.lib.python2.7.site-packages.pip._vendor',
              'venv.lib.python2.7.site-packages.pip._vendor.distlib',
              'venv.lib.python2.7.site-packages.pip._vendor.distlib._backport',
              'venv.lib.python2.7.site-packages.pip._vendor.colorama',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib._trie',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.filters',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treewalkers',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treeadapters',
              'venv.lib.python2.7.site-packages.pip._vendor.html5lib.treebuilders',
              'venv.lib.python2.7.site-packages.pip._vendor.lockfile',
              'venv.lib.python2.7.site-packages.pip._vendor.progress',
              'venv.lib.python2.7.site-packages.pip._vendor.requests',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.chardet',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.util',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.contrib',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.packages',
              'venv.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.packages.ssl_match_hostname',
              'venv.lib.python2.7.site-packages.pip._vendor.packaging',
              'venv.lib.python2.7.site-packages.pip._vendor.cachecontrol',
              'venv.lib.python2.7.site-packages.pip._vendor.cachecontrol.caches',
              'venv.lib.python2.7.site-packages.pip._vendor.webencodings',
              'venv.lib.python2.7.site-packages.pip._vendor.pkg_resources',
              'venv.lib.python2.7.site-packages.pip.commands', 'venv.lib.python2.7.site-packages.pip.operations',
              'venv.lib.python2.7.site-packages.idna', 'venv.lib.python2.7.site-packages.lxml',
              'venv.lib.python2.7.site-packages.lxml.html', 'venv.lib.python2.7.site-packages.lxml.includes',
              'venv.lib.python2.7.site-packages.lxml.isoschematron', 'venv.lib.python2.7.site-packages.nltk',
              'venv.lib.python2.7.site-packages.nltk.app', 'venv.lib.python2.7.site-packages.nltk.ccg',
              'venv.lib.python2.7.site-packages.nltk.sem', 'venv.lib.python2.7.site-packages.nltk.tag',
              'venv.lib.python2.7.site-packages.nltk.tbl', 'venv.lib.python2.7.site-packages.nltk.chat',
              'venv.lib.python2.7.site-packages.nltk.draw', 'venv.lib.python2.7.site-packages.nltk.misc',
              'venv.lib.python2.7.site-packages.nltk.stem', 'venv.lib.python2.7.site-packages.nltk.test',
              'venv.lib.python2.7.site-packages.nltk.test.unit',
              'venv.lib.python2.7.site-packages.nltk.test.unit.translate',
              'venv.lib.python2.7.site-packages.nltk.chunk', 'venv.lib.python2.7.site-packages.nltk.parse',
              'venv.lib.python2.7.site-packages.nltk.corpus', 'venv.lib.python2.7.site-packages.nltk.corpus.reader',
              'venv.lib.python2.7.site-packages.nltk.cluster', 'venv.lib.python2.7.site-packages.nltk.metrics',
              'venv.lib.python2.7.site-packages.nltk.twitter', 'venv.lib.python2.7.site-packages.nltk.classify',
              'venv.lib.python2.7.site-packages.nltk.tokenize', 'venv.lib.python2.7.site-packages.nltk.inference',
              'venv.lib.python2.7.site-packages.nltk.sentiment', 'venv.lib.python2.7.site-packages.nltk.translate',
              'venv.lib.python2.7.site-packages.click', 'venv.lib.python2.7.site-packages.flask',
              'venv.lib.python2.7.site-packages.flask.ext', 'venv.lib.python2.7.site-packages.wheel',
              'venv.lib.python2.7.site-packages.wheel.tool', 'venv.lib.python2.7.site-packages.wheel.signatures',
              'venv.lib.python2.7.site-packages.jinja2', 'venv.lib.python2.7.site-packages.certifi',
              'venv.lib.python2.7.site-packages.chardet', 'venv.lib.python2.7.site-packages.chardet.cli',
              'venv.lib.python2.7.site-packages.urllib3', 'venv.lib.python2.7.site-packages.urllib3.util',
              'venv.lib.python2.7.site-packages.urllib3.contrib',
              'venv.lib.python2.7.site-packages.urllib3.contrib._securetransport',
              'venv.lib.python2.7.site-packages.urllib3.packages',
              'venv.lib.python2.7.site-packages.urllib3.packages.backports',
              'venv.lib.python2.7.site-packages.urllib3.packages.ssl_match_hostname',
              'venv.lib.python2.7.site-packages.dateutil', 'venv.lib.python2.7.site-packages.dateutil.tz',
              'venv.lib.python2.7.site-packages.dateutil.zoneinfo', 'venv.lib.python2.7.site-packages.psycopg2',
              'venv.lib.python2.7.site-packages.psycopg2.tests', 'venv.lib.python2.7.site-packages.requests',
              'venv.lib.python2.7.site-packages.textblob', 'venv.lib.python2.7.site-packages.textblob.en',
              'venv.lib.python2.7.site-packages.textblob.unicodecsv', 'venv.lib.python2.7.site-packages.werkzeug',
              'venv.lib.python2.7.site-packages.werkzeug.debug', 'venv.lib.python2.7.site-packages.werkzeug.contrib',
              'venv.lib.python2.7.site-packages.flask_cors', 'venv.lib.python2.7.site-packages.markupsafe',
              'venv.lib.python2.7.site-packages.setuptools', 'venv.lib.python2.7.site-packages.setuptools.extern',
              'venv.lib.python2.7.site-packages.setuptools.command', 'venv.lib.python2.7.site-packages.pkg_resources',
              'venv.lib.python2.7.site-packages.pkg_resources.extern',
              'venv.lib.python2.7.site-packages.pkg_resources._vendor',
              'venv.lib.python2.7.site-packages.pkg_resources._vendor.packaging',
              'venv.lib.python2.7.site-packages.fake_useragent', 'venv.lib.python2.7.site-packages.singleton_decorator',
              'venv.local.lib.python2.7.site-packages.bs4', 'venv.local.lib.python2.7.site-packages.bs4.tests',
              'venv.local.lib.python2.7.site-packages.bs4.builder', 'venv.local.lib.python2.7.site-packages.pip',
              'venv.local.lib.python2.7.site-packages.pip.req', 'venv.local.lib.python2.7.site-packages.pip.vcs',
              'venv.local.lib.python2.7.site-packages.pip.utils', 'venv.local.lib.python2.7.site-packages.pip.compat',
              'venv.local.lib.python2.7.site-packages.pip.models', 'venv.local.lib.python2.7.site-packages.pip._vendor',
              'venv.local.lib.python2.7.site-packages.pip._vendor.distlib',
              'venv.local.lib.python2.7.site-packages.pip._vendor.distlib._backport',
              'venv.local.lib.python2.7.site-packages.pip._vendor.colorama',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib._trie',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib.filters',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib.treewalkers',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib.treeadapters',
              'venv.local.lib.python2.7.site-packages.pip._vendor.html5lib.treebuilders',
              'venv.local.lib.python2.7.site-packages.pip._vendor.lockfile',
              'venv.local.lib.python2.7.site-packages.pip._vendor.progress',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.chardet',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.util',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.contrib',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.packages',
              'venv.local.lib.python2.7.site-packages.pip._vendor.requests.packages.urllib3.packages.ssl_match_hostname',
              'venv.local.lib.python2.7.site-packages.pip._vendor.packaging',
              'venv.local.lib.python2.7.site-packages.pip._vendor.cachecontrol',
              'venv.local.lib.python2.7.site-packages.pip._vendor.cachecontrol.caches',
              'venv.local.lib.python2.7.site-packages.pip._vendor.webencodings',
              'venv.local.lib.python2.7.site-packages.pip._vendor.pkg_resources',
              'venv.local.lib.python2.7.site-packages.pip.commands',
              'venv.local.lib.python2.7.site-packages.pip.operations', 'venv.local.lib.python2.7.site-packages.idna',
              'venv.local.lib.python2.7.site-packages.lxml', 'venv.local.lib.python2.7.site-packages.lxml.html',
              'venv.local.lib.python2.7.site-packages.lxml.includes',
              'venv.local.lib.python2.7.site-packages.lxml.isoschematron',
              'venv.local.lib.python2.7.site-packages.nltk', 'venv.local.lib.python2.7.site-packages.nltk.app',
              'venv.local.lib.python2.7.site-packages.nltk.ccg', 'venv.local.lib.python2.7.site-packages.nltk.sem',
              'venv.local.lib.python2.7.site-packages.nltk.tag', 'venv.local.lib.python2.7.site-packages.nltk.tbl',
              'venv.local.lib.python2.7.site-packages.nltk.chat', 'venv.local.lib.python2.7.site-packages.nltk.draw',
              'venv.local.lib.python2.7.site-packages.nltk.misc', 'venv.local.lib.python2.7.site-packages.nltk.stem',
              'venv.local.lib.python2.7.site-packages.nltk.test',
              'venv.local.lib.python2.7.site-packages.nltk.test.unit',
              'venv.local.lib.python2.7.site-packages.nltk.test.unit.translate',
              'venv.local.lib.python2.7.site-packages.nltk.chunk', 'venv.local.lib.python2.7.site-packages.nltk.parse',
              'venv.local.lib.python2.7.site-packages.nltk.corpus',
              'venv.local.lib.python2.7.site-packages.nltk.corpus.reader',
              'venv.local.lib.python2.7.site-packages.nltk.cluster',
              'venv.local.lib.python2.7.site-packages.nltk.metrics',
              'venv.local.lib.python2.7.site-packages.nltk.twitter',
              'venv.local.lib.python2.7.site-packages.nltk.classify',
              'venv.local.lib.python2.7.site-packages.nltk.tokenize',
              'venv.local.lib.python2.7.site-packages.nltk.inference',
              'venv.local.lib.python2.7.site-packages.nltk.sentiment',
              'venv.local.lib.python2.7.site-packages.nltk.translate', 'venv.local.lib.python2.7.site-packages.click',
              'venv.local.lib.python2.7.site-packages.flask', 'venv.local.lib.python2.7.site-packages.flask.ext',
              'venv.local.lib.python2.7.site-packages.wheel', 'venv.local.lib.python2.7.site-packages.wheel.tool',
              'venv.local.lib.python2.7.site-packages.wheel.signatures',
              'venv.local.lib.python2.7.site-packages.jinja2', 'venv.local.lib.python2.7.site-packages.certifi',
              'venv.local.lib.python2.7.site-packages.chardet', 'venv.local.lib.python2.7.site-packages.chardet.cli',
              'venv.local.lib.python2.7.site-packages.urllib3', 'venv.local.lib.python2.7.site-packages.urllib3.util',
              'venv.local.lib.python2.7.site-packages.urllib3.contrib',
              'venv.local.lib.python2.7.site-packages.urllib3.contrib._securetransport',
              'venv.local.lib.python2.7.site-packages.urllib3.packages',
              'venv.local.lib.python2.7.site-packages.urllib3.packages.backports',
              'venv.local.lib.python2.7.site-packages.urllib3.packages.ssl_match_hostname',
              'venv.local.lib.python2.7.site-packages.dateutil', 'venv.local.lib.python2.7.site-packages.dateutil.tz',
              'venv.local.lib.python2.7.site-packages.dateutil.zoneinfo',
              'venv.local.lib.python2.7.site-packages.psycopg2',
              'venv.local.lib.python2.7.site-packages.psycopg2.tests',
              'venv.local.lib.python2.7.site-packages.requests', 'venv.local.lib.python2.7.site-packages.textblob',
              'venv.local.lib.python2.7.site-packages.textblob.en',
              'venv.local.lib.python2.7.site-packages.textblob.unicodecsv',
              'venv.local.lib.python2.7.site-packages.werkzeug',
              'venv.local.lib.python2.7.site-packages.werkzeug.debug',
              'venv.local.lib.python2.7.site-packages.werkzeug.contrib',
              'venv.local.lib.python2.7.site-packages.flask_cors', 'venv.local.lib.python2.7.site-packages.markupsafe',
              'venv.local.lib.python2.7.site-packages.setuptools',
              'venv.local.lib.python2.7.site-packages.setuptools.extern',
              'venv.local.lib.python2.7.site-packages.setuptools.command',
              'venv.local.lib.python2.7.site-packages.pkg_resources',
              'venv.local.lib.python2.7.site-packages.pkg_resources.extern',
              'venv.local.lib.python2.7.site-packages.pkg_resources._vendor',
              'venv.local.lib.python2.7.site-packages.pkg_resources._vendor.packaging',
              'venv.local.lib.python2.7.site-packages.fake_useragent',
              'venv.local.lib.python2.7.site-packages.singleton_decorator', 'server', 'server.app', 'server.app.views',
              'server.app.common', 'server.app.common.db', 'server.app.models', 'server.app.models.config',
              'server.mock'],
    url='https://github.com/ExpertsVision/crawper',
    license='GPL',
    author='awakeel',
    author_email='awkhan978@gmail.com',
    description='Amazon Scraper based on BS4, Flask and PostgreSQL'
)
