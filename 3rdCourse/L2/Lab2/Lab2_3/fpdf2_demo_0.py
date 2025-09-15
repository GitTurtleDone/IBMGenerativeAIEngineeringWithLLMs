import copy
import os
import tempfile
from datetime import datetime
import shutil
import re
import textwrap
#
from fpdf import FPDF, FontFace, TextStyle
from fpdf.enums import XPos, YPos
from fpdf.table import (
    Align,
    CellBordersLayout,
    MethodReturnValue,
    TableBordersLayout,
    TableCellFillMode,
    TableHeadingsDisplay,
    TableSpan,
    VAlign,
    WrapMode,
)
from fpdf import FPDF, TextStyle
#
from mocked_data import LIST_IPSO


RUNNING_ON_RICHARDS_MACHINE = True


class GiangOne(FPDF):
    '''
    Utility class to experiment with J's
    PDF issue
    '''

    def __init__(   self,
                    list_ipso,
                    list_modes_to_execute,
                    *args,
                    **kwargs):

        super().__init__(*args, **kwargs)

        self.list_modes_to_execute = list_modes_to_execute
        #
        self.list_ipso = list_ipso
        self.set_font("Arial", "", 9)
        #
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.avg_char_width = self.get_string_width(alphabet) / len(alphabet)
        #
        self.colors = [
            (220, 20, 60),   # Crimson
            (30, 144, 255),  # Dodger Blue
            (34, 139, 34),   # Forest Green
            (255, 140, 0),   # Dark Orange
            (128, 0, 128),   # Purple
        ]


    def footer(self):
        # Position footer 15 mm from bottom
        self.set_y(-15)
        # Choose font
        self.set_font("Arial", style="I", size=8)
        # Text color (dark gray)
        self.set_text_color(50, 50, 50)

        # Page number: {nb} is replaced with total page count
        page_text = f"Page {self.page_no()} of {{nb}}"
        self.cell(0, 10, page_text, align="C")


    def output_mode_0(self):
        for ipso_para in self.list_ipso:
            with self.unbreakable() as para:
                para.multi_cell(0, 10, text=ipso_para)


    def output_mode_1(self):
        for ipso_para in self.list_ipso:
            wrapped_ipso_para = textwrap.fill(ipso_para, width = 160)
            self.multi_cell(160, 6, wrapped_ipso_para, align='L')


    def output_mode_2(self):
        for ipso_para in self.list_ipso:
            self.multi_cell(160, 6, ipso_para, align='L')


    def output_mode_3(self):
        '''
        Experimenting with line width
        '''
        line_width_chars = 80
        line_width_mm = line_width_chars * self.avg_char_width

        for ipso_para in self.list_ipso:
            self.multi_cell(line_width_mm, h=6, text=ipso_para, align='L')
            self.ln(10)

    def output_mode_4(self):
        '''
        Colour the output paragraphs to make it clearer
        what's going on
        '''


        line_width_chars = 80
        line_width_mm = line_width_chars * self.avg_char_width
        #
        for i, ipso_para in enumerate(self.list_ipso):
            # Pick a color, cycling through the list if more than 5 paragraphs
            r, g, b = self.colors[i % len(self.colors)]
            self.set_text_color(r, g, b)
            #
            self.multi_cell(line_width_mm, 6, text=ipso_para, align="L")
            #
            self.ln(10)

        self.set_text_color(42, 31, 34)



def get_a_temp_path():
    # Create a timestamped filename in the temp directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = tempfile.gettempdir()
    output_file_path = os.path.join(temp_dir, f"fpdf2_giang_experiment_{timestamp}.pdf")
    return output_file_path

def main(lst_ipso):
    pdf = GiangOne(lst_ipso, [4,3])
    #
    pdf.add_page()
    #
    if 4 in pdf.list_modes_to_execute:
        pdf.output_mode_4()
        #
        pdf.add_page()
    #
    if 3 in pdf.list_modes_to_execute:
        pdf.output_mode_3()
        #
        pdf.add_page()
        #
    if 2 in pdf.list_modes_to_execute:
        pdf.output_mode_2()
        #
        pdf.add_page()
        #
    if 1 in pdf.list_modes_to_execute:
        pdf.output_mode_1()
        #
        pdf.add_page()
        #
    if 0 in pdf.list_modes_to_execute:
        pdf.output_mode_0()
        #

    output_file_path = get_a_temp_path()
    # Render the page to the specified file
    pdf.output(output_file_path)
    # Output the path of the file
    print(f"Output written to: {output_file_path}")
    #
    if RUNNING_ON_RICHARDS_MACHINE:
        # Prompt the user to copy the output file
        user_input = input(f"Copy output to /mnt/c/Users/Richard Shea/Desktop/fpdf2-test-output-material-temp-only? [Y/N] (default: Y): ") or 'Y'
        #
        if user_input.upper() == 'Y':
            destination_path = "/mnt/c/Users/Richard Shea/Desktop/fpdf2-test-output-material-temp-only"
            shutil.copy2(output_file_path, destination_path)
            print(f"File copied to: {destination_path}")    



if __name__ == "__main__":
    main(LIST_IPSO)
