# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests

from pages.desktop.about import AboutPage


class TestAboutPage:

    @pytest.mark.nondestructive
    def test_footer_link_destinations_are_correct(self, base_url, selenium):
        page = AboutPage(base_url, selenium).open()
        bad_links = []
        for link in AboutPage.Footer.footer_links_list:
            url = page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        assert [] == bad_links

    @pytest.mark.nondestructive
    def test_major_link_destinations_are_correct(self, base_url, selenium):
        page = AboutPage(base_url, selenium).open()
        bad_links = []
        for link in page.major_links_list:
            url = page.link_destination(link.get('locator'))
            if not url.endswith(link.get('url_suffix')):
                bad_links.append('%s does not end with %s' % (url, link.get('url_suffix')))
        assert [] == bad_links

    @pytest.mark.nondestructive
    def test_sign_up_form_links(self, base_url, selenium):
        page = AboutPage(base_url, selenium).open()
        page.expand_sign_up_form()
        page.wait_for_element_visible(*page._sign_up_form_privacy_checkbox_locator)
        for link in page.sign_up_form_link_list:
            assert page.is_element_visible(*link.get('locator'))
            url = page.link_destination(link.get('locator'))
            assert url.endswith(link.get('url_suffix'))
            assert requests.codes.ok == page.get_response_code(url)
