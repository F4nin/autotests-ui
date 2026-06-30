from operator import index
from time import sleep

import pytest
from pages.courses.courses_list_page import CoursesListPage
from pages.courses.create_course_page import CreateCoursePage
@pytest.mark.ui
@pytest.mark.courses
@pytest.mark.regression
class TestCourses:

    def test_empty_courses_list(self, courses_list_page: CoursesListPage):
        courses_list_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

        courses_list_page.navbar.check_visible('username')
        courses_list_page.sidebar.check_visible()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.check_visible_empty_view()

    @pytest.mark.parametrize(
        'title, estimated_time, description, max_score, min_score',
        [
            ("Playwright Basics", "2 weeks", "Introduction to Playwright", "100", "10"),
            ("Playwright Advanced", "4 weeks", "Advanced Playwright course", "100", "40"),
        ]
    )
    def test_create_course(self, courses_list_page: CoursesListPage, create_course_page: CreateCoursePage, title,
                           estimated_time, description, max_score, min_score):
        create_course_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create")

        create_course_page.create_course_toolbar_view.check_visible()
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=False)
        create_course_page.create_course_form.check_visible(
            title="", max_score="0", min_score="0", description="", estimated_time=""
        )

        create_course_page.create_course_exercises_toolbar_view.check_visible()
        create_course_page.check_visible_exercises_empty_view()

        create_course_page.image_upload_widget.upload_preview_image("./testdata/files/image.png")
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.create_course_form.fill(
            title=title,
            max_score=max_score,
            min_score=min_score,
            description=description,
            estimated_time=estimated_time
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0, title=title, max_score=max_score, min_score=min_score, estimated_time=estimated_time
        )

    @pytest.mark.parametrize(
        'title, estimated_time, description, max_score, min_score, new_title, new_estimated_time,new_description, new_max_score, new_min_score',
        [
            ("Playwright Basics", "2 weeks", "Introduction to Playwright", "100", "10", "Playwright Advanced", "4 weeks", "Advanced Playwright course", "100", "40"),
        ]
    )
    def test_edit_course(
            self,
            courses_list_page: CoursesListPage,
            create_course_page: CreateCoursePage,
            title,
            estimated_time,
            description,
            max_score,
            min_score,
            new_title,
            new_max_score,
            new_min_score,
            new_description,
            new_estimated_time,
    ):

        create_course_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create")
        create_course_page.image_upload_widget.upload_preview_image("./testdata/files/image.png")
        create_course_page.image_upload_widget.check_visible(is_image_uploaded=True)
        create_course_page.create_course_form.fill(
            title=title,
            max_score=max_score,
            min_score=min_score,
            description=description,
            estimated_time=estimated_time
        )

        create_course_page.create_course_toolbar_view.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0, title=title, max_score=max_score, min_score=min_score, estimated_time=estimated_time
        )
        courses_list_page.course_view.menu.click_edit(index=0)
        create_course_page.create_course_form.fill(
            title=new_title,
            max_score=new_max_score,
            min_score=new_min_score,
            description=new_description,
            estimated_time=new_estimated_time
        )
        create_course_page.create_course_toolbar_view.click_create_course_button()

        courses_list_page.toolbar_view.check_visible()
        courses_list_page.course_view.check_visible(
            index=0, title=new_title, max_score=new_max_score, min_score=new_min_score, estimated_time=new_estimated_time
        )






