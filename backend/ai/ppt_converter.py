import os
import tempfile
import pythoncom
import win32com.client


def convert_ppt_to_pptx(ppt_path):

    pythoncom.CoInitialize()

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 0

    presentation = powerpoint.Presentations.Open(
        os.path.abspath(ppt_path),
        WithWindow=False
    )

    temp_dir = tempfile.gettempdir()

    output = os.path.join(
        temp_dir,
        os.path.splitext(os.path.basename(ppt_path))[0] + ".pptx"
    )

    presentation.SaveAs(output, 24)   # 24 = pptx

    presentation.Close()
    powerpoint.Quit()

    return output