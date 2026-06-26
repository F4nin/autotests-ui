from playwright.sync_api import Page, expect

from components.courses.course_view_component import CourseViewComponent
from components.navigation.navbar_component import NavbarComponent
from components.navigation.sidebar_component import SidebarComponent
from components.views.empty_view_component import EmptyViewComponent
from pages.base_page import BasePage

class CoursesListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = NavbarComponent(page)
        self.sidebar = SidebarComponent(page)
        self.empty_view = EmptyViewComponent(page, 'courses-list')
        self.course_view = CourseViewComponent(page)

        self.courses_title = page.get_by_test_id('courses-list-toolbar-title-text')
        self.courses_button = page.get_by_test_id('courses-list-toolbar-create-course-button')

    def check_visible_courses_title(self):
        expect(self.courses_title).to_be_visible()
        expect(self.courses_title).to_have_text('Courses')

    def check_courses_button(self):
        expect(self.courses_button).to_be_visible()

    def check_visible_empty_view(self):
        self.empty_view.check_visible(
            title='There is no results',
            description='Results from the load test pipeline will be displayed here'
        )
