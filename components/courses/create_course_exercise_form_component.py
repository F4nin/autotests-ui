from playwright.sync_api import Page, expect

from components.base_component import BaseComponent


class CreateCourseExerciseFormComponent(BaseComponent):

    def click_delete_button(self, index: int):
        # Обратите внимание, что локатор инициализируется непосредственно в методе.
        # Это временное решение, так как с классическим подходом POM сложно работать с динамическими локаторами.
        # В текущей реализации мы не можем заранее объявить локатор на уровне класса, поскольку его значение
        # зависит от переданного индекса.
        # В дальнейшем мы будем использовать паттерн PageFactory для более удобной обработки таких случаев
        # и динамических элементов на странице.
        delete_button = self.page.get_by_test_id(
            f"create-course-exercise-{index}-box-toolbar-delete-exercise-button"
        )
        delete_button.click()

    def check_visible(self, index: int, title: str, description: str):
        subtitle = self.page.get_by_test_id(
            f"create-course-exercise-{index}-box-toolbar-subtitle-text"
        )
        title_input = self.page.get_by_test_id(
            f"create-course-exercise-form-title-{index}-input"
        )
        description_input = self.page.get_by_test_id(
            f"create-course-exercise-form-description-{index}-input"
        )

        expect(subtitle).to_be_visible()
        expect(subtitle).to_have_text(f"#{index + 1} Exercise")

        expect(title_input).to_be_visible()
        expect(title_input).to_have_value(title)

        expect(description_input).to_be_visible()
        expect(description_input).to_have_value(description)

    def fill_create_form(self, index: int, title: str, description: str):
        title_input = self.page.get_by_test_id(
            f"create-course-exercise-form-title-{index}-input"
        )
        description_input = self.page.get_by_test_id(
            f"create-course-exercise-form-description-{index}-input"
        )

        title_input.fill(title)
        expect(title_input).to_have_value(title)

        description_input.fill(description)
        expect(description_input).to_have_value(description)