from django.test import TestCase
from django.contrib.sites.models import Site
from selenium import webdriver
from store.forms import ServiceReviewForm

site = Site.objects.get_current().domain


# class FunctionalTestCase(TestCase):
#     """
#         Tests need to be start with `test_`
#     """
#
#     def setUp(self):
#         """ Get browser ready"""
#         self.browser = webdriver.Chrome()
#         self.browser.set_window_size(1024, 768)
#
#     def test_homepage(self):
#         """ Test for homepage """
#         self.browser.get(site)
#         self.assertIn('Quality Printing', self.browser.page_source)
#
#     def test_search(self):
#         """ Test search """
#         self.browser.get(site)
#         # find search box
#         search_box = self.browser.find_element_by_id('searchBox')
#         # input Poster A4
#         search_box.send_keys('Poster A4')
#         # click on search icon
#         self.browser.find_element_by_id('searchIcon').click()
#         self.assertIn('Poster A4', self.browser.page_source)
#
#     def tearDown(self):
#         """ Close browser """
#         self.browser.quit()


class UnitTestCase(TestCase):

    def test_homepage_template(self):
        """ Test homepage rendering """
        response = self.client.get(site)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_service_review_form(self):
        """ Test service review form """
        form = ServiceReviewForm(data={
            'review': 'My test review',
            'rating': 3
        })
        self.assertTrue(form.is_valid())

