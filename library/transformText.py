
class transformer:
    def __init__(self) -> None:
        pass

    def text_helper(text):
            max_length = 1100
            step = 100
            result = []
            start_index = 0

            while start_index < len(text):
                end_index = start_index + max_length + 100
                if end_index >= len(text):
                    end_index = len(text)

                window = text[start_index:end_index]
                if len(window) < 400:
                    result[-1] = result[-1].replace('\n', '') + window
                    break
                checked_index_window = window.find('다.', max_length - step ,max_length + step)

                if checked_index_window != -1:
                    newline_index = checked_index_window + start_index + 2
                    result.append(text[start_index:newline_index] + '\n')
                    start_index = newline_index
                else:
                    result.append(text[start_index:end_index] + '\n')
                    start_index = end_index
            return ''.join(result)