import re


class FileUtils:
    @staticmethod
    def strip_rows(command_output):
        multiline_str = ''
        for out_row in command_output.splitlines():
            multiline_str += out_row.rstrip() + '\n'
        return multiline_str;

    @staticmethod
    def remove_skip_rows(multiline_str, skip_str_array, skip_empty_lines):
        outr = ''
        for out_row in multiline_str.splitlines():
            found = 0
            for s in skip_str_array:
                if s in out_row:
                    found = 1
            if found == 0 and \
                    (not skip_empty_lines or (skip_empty_lines and out_row.rstrip() != "")):
                outr += out_row + '\n'
        return outr;

    @staticmethod
    def check_header_string_regexp(multiline_str, header_str_regexp):
        regexp = re.compile(header_str_regexp)
        for out_row in multiline_str.splitlines():
            if regexp.search(out_row) is not None:
                return True, out_row
        return False, ""

    @staticmethod
    def check_header_string_array(multiline_str, header_str_array):
        for idx, val in enumerate(header_str_array):
            if val + '\n' in multiline_str:
                return True, val
        return False, ""

    @staticmethod
    def remove_before_header_string(multiline_str, header_str):
        return multiline_str[multiline_str.find(header_str + '\n') + len(header_str + '\n'):]

    @staticmethod
    def remove_after_footer_string(multiline_str, footer_str):
        return multiline_str[:multiline_str.find(footer_str)]

    @staticmethod
    def extract_block(multiline_str, starting_row, ending_row, add_ending_row):
        copy = False
        outr = ''
        for line in multiline_str.splitlines():
            line = line.rstrip()
            if line == starting_row:
                copy = True
            elif line == ending_row:
                if add_ending_row:
                    outr += line + '\n'
                copy = False

            if copy:
                outr += line + '\n'
        return outr

    @staticmethod
    def add_char_to_every_row_if_not_exist(multiline_str, character):
        str2 = ''
        for out_row in multiline_str.splitlines():
            str2 += out_row + (character if character not in out_row else '') + '\n'
        return str2

    @staticmethod
    def parse_extact_table(multiline_str, header_column_position):
        result = []
        for out_result_row in multiline_str.splitlines():
            arr = []
            for i in range(0, len(header_column_position)):
                start_pos = header_column_position[i][0]
                if header_column_position[i][1] is None:
                    if i < len(header_column_position) - 1:
                        end_pos = header_column_position[i + 1][0] - 1
                    else:
                        end_pos = len(out_result_row)
                else:
                    end_pos = header_column_position[i][1] - 1
                d = out_result_row[start_pos:end_pos].strip()
                arr.append(d)
            result.append(arr)

        if len(result) == 0:
            raise Exception('TI_Utilis', 'No param list (' + str + ')')
        return result

    @staticmethod
    def create_htmltable(command_output_array_table, first_row_html_header):
        """
           Add to output windows an HTML table with the command
        :param context:
        :param command_output:
        """
        str = '<table style="color:black" border="1" cellpadding="5">'
        str += '<thead>'
        if first_row_html_header:
            if len(command_output_array_table) > 0:
                for th in command_output_array_table[0]:
                    str += '<th>' + th + '</th>'
        str += '</thead>'

        str += '<tbody>'
        for idx, row in enumerate(command_output_array_table):
            if not first_row_html_header or idx > 0:
                str += '<tr>'

                for val in row:
                    str += '<td>' + val + '</td>'
                str += '</tr>'
        str += '</tbody></table>'
        return str;
