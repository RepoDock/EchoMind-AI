import os
import tempfile
import pythoncom
import win32com.client


def convert_ppt_to_pptx(ppt_path):


    pythoncom.CoInitialize()

    powerpoint = None
    presentation = None

    try:

        powerpoint = win32com.client.DispatchEx("PowerPoint.Application")
        powerpoint.Visible = True

        presentation = powerpoint.Presentations.Open(
            FileName=os.path.abspath(ppt_path),
            ReadOnly=True
        )

        temp_dir = tempfile.gettempdir()

        output = os.path.join(
            temp_dir,
            os.path.splitext(os.path.basename(ppt_path))[0] + ".pptx"
        )

        presentation.SaveAs(output, 24)


        return output

    except Exception as e:
        print(f" PPT Convert Failed: {e}")
        return None

    finally:
        if presentation:
            presentation.Close()

        if powerpoint:
            powerpoint.Quit()

        pythoncom.CoUninitialize()