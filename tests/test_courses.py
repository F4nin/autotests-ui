import pytest
from pages.courses_list_page import CoursesListPage
from pages.create_course_page import CreateCoursePage


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.courses
def test_empty_courses_list(courses_page: CoursesListPage):
    courses_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")

    courses_page.navbar.check_visible('username')
    courses_page.sidebar.check_visible()

    courses_page.toolbar_view.check_visible()
    courses_page.check_visible_empty_view()


@pytest.mark.courses
@pytest.mark.regression
@pytest.mark.parametrize(
    'title, estimated_time, description, max_score, min_score',
     [
         ("Playwright Basics", "2 weeks", "Introduction to Playwright", "100", "10"),
         ("Playwright Advanced", "4 weeks", "Advanced Playwright course", "100", "40"),
     ]
)
def test_create_course(courses_page: CoursesListPage, create_course_page: CreateCoursePage, title, estimated_time, description, max_score, min_score):
    create_course_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses/create')
    create_course_page.check_visible_create_course_title()
    create_course_page.check_disabled_create_course_button()
    create_course_page.check_visible_image_preview_empty_view()
    create_course_page.check_visible_image_upload_view(is_image_uploaded=False)
    create_course_page.check_visible_create_course_form(
        title='',
        estimated_time='',
        description='',
        max_score="0",
        min_score="0"
    )
    create_course_page.check_visible_exercises_title()
    create_course_page.check_visible_create_exercise_button()
    create_course_page.check_visible_exercises_empty_view()
    create_course_page.upload_preview_image('./testdata/files/image.png')
    create_course_page.check_visible_image_upload_view(is_image_uploaded=True)
    create_course_page.fill_create_course_form(
        title=title,
        estimated_time=estimated_time,
        description=description,
        max_score=max_score,
        min_score=min_score
    )
    create_course_page.click_create_course_button()
    courses_page.toolbar_view.check_visible()
    courses_page.course_view.check_visible(
        index=0,
        title=title,
        estimated_time=estimated_time,
        max_score=max_score,
        min_score=min_score
    )







