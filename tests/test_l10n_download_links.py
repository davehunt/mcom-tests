# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bs4 import BeautifulSoup
import pytest
import requests

pytestmark = [pytest.mark.nondestructive, pytest.mark.skip_selenium]


def pytest_generate_tests(metafunc):
    base_url = metafunc.config.option.base_url
    page = metafunc.cls.page  # get the target page from the test class
    r = requests.get('{0}{1}'.format(base_url, page))
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_='build-table')  # find the table of links
    idlist = []
    argvalues = []
    for row in table.find('tbody').find_all('tr'):
        locale = row['id']
        idlist.append(locale)  # the test id should be the locale
        url = row.find('a')['href']
        argvalues.append((locale, url))  # pass locale and url to each test
    metafunc.parametrize('locale, url', argvalues, ids=idlist)


def check_link(locale, url):
    r = requests.head(url, allow_redirects=True)
    assert locale in r.url  # the correct locale is in the final url
    assert requests.codes.found == r.history[0].status_code  # url redirects


class TestFirefoxAll(object):
    page = '/firefox/all/'

    def test_download_link(self, locale, url):
        check_link(locale, url)


class TestFirefoxOrganizationsAll(object):
    page = '/firefox/organizations/all/'

    def test_download_link(self, locale, url):
        check_link(locale, url)


class TestThunderbirdAll(object):
    page = '/thunderbird/all/'

    def test_download_link(self, locale, url):
        check_link(locale, url)
