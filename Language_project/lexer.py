import re

class Lexer:
    def __init__(self, code):
        """ Initialize the lexer with the code to tokenize. """
        self.code = code
        self.tokens = []
        self.current_position = 0
        self.line_number = 1

    def tokenize(self):
        """ Convert the input string into a list of tokens. """
        TOKEN_REGEX = self._compile_token_regex()
        for match in re.finditer(TOKEN_REGEX, self.code):
            kind = match.lastgroup
            value = match.group(kind)
            if kind == "SKIP":
                # Skip whitespace and comments
                continue
            elif kind == "NEWLINE":
                # Increment line number counter
                self.line_number += 1
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character {value!r} at line {self.line_number}")
            else:
                token = (kind, value)
                self.tokens.append(token)
        return self.tokens

    def _compile_token_regex(self):
        """ Utility method to compile the token regex. """
        token_specification = [
            ("NUMBER", r"\d+(\.\d*)?"),       # Integer or decimal number
            ("ASSIGN", r"="),                 # Assignment operator
            ("SEMICOLON", r";"),              # Semicolon (end of statement)
            ("ID", r"[a-zA-Z_]\w*"),          # Identifiers
            ("OP", r"[+\-*/%]"),              # Arithmetic operators
            ("LPAREN", r"\("),                # Left parenthesis
            ("RPAREN", r"\)"),                # Right parenthesis
            ("IF", r"if"),                    # 'if' keyword
            ("LOOP", r"loop"),                # 'loop' keyword
            ("END_IF", r"end_if"),            # 'end_if' keyword
            ("END_LOOP", r"end_loop"),        # 'end_loop' keyword
            ("LOGIC_OP", r"==|!=|>|<|>=|<="), # Logical operators
            ("NEWLINE", r"\n"),               # Line endings
            ("SKIP", r"[ \t]+"),              # Skip over spaces and tabs
            ("MISMATCH", r"."),               # Any other character
        ]
        regex_patterns = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
        return re.compile(regex_patterns, re.MULTILINE)

# Example usage of the lexer
if __name__ == "__main__":
    input_code = """
    program
    value = 32;
    mod1 = 45;
    z = mod1 / value * (value % 7) + mod1;
    loop (i = 0 : value)
    z = z + mod1;
    end_loop
    if (z >= 50)
    newValue = 50 / mod1;
    x = mod1;
    end_if
    end_program
    """
    lexer = Lexer(input_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
