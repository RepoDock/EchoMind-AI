from pptx import Presentation


def extract_ppt_text(file_path):

    presentation = Presentation(file_path)

    text = ""

    for slide in presentation.slides:

        print("Slide")

        for shape in slide.shapes:

            print(shape.shape_type)

            if hasattr(shape, "text"):

                print(shape.text)

                text += shape.text + "\n"

    return text