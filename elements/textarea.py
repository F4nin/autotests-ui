from playwright.sync_api import expect

from elements.base_element import BaseElement


class TextAreaInput(BaseElement):
    def get_locator(self, **kwargs):
        return super().get_locator(**kwargs).locator('textarea')
    
    def fill(self, value: str, **kwargs):
        locator = self.get_locator(**kwargs)
        locator.fill(value)

    def check_have_value(self, value: str, **kwargs):
        locator = self.get_locator(**kwargs)
        expect(locator). to_have_value(value)