from Language_project.lexer import Lexer

class ParserError(Exception):
    """ Custom exception for parser errors. """
    def __init__(self, message, token):
        super().__init__(f"{message}: {token}")
        self.token = token

class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = 0
        self.advance()

    def advance(self):
        """ Advance to the next token. """
        try:
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        except IndexError:
            self.current_token = None

    def parse(self):
        """ Parse the entire program. """
        self.program()
        if self.current_token is not None:
            raise ParserError("Extra input after end of program", self.current_token)
        print("Parsing completed successfully.")

    def program(self):
        """ <program> ::= "program" <statements> "end_program" """
        self.eat('ID', 'program')
        self.statements()
        self.eat('ID', 'end_program')

    def statements(self):
        """ <statements> ::= { <statement> } """
        while self.current_token and self.current_token[0] != 'ID' or self.current_token[1] not in ['end_program', 'end_if', 'end_loop']:
            self.statement()

    def statement(self):
        """ Handle a single statement which could be an assignment, condition, or loop. """
        if self.current_token[1] in ['if']:
            self.condition()
        elif self.current_token[1] in ['loop']:
            self.loop()
        else:
            self.assignment()
            self.eat('SEMICOLON')

    def assignment(self):
        """ <assignment> ::= <identifier> "=" <expression> """
        self.eat('ID')
        self.eat('ASSIGN')
        self.expression()

    def condition(self):
        """ <condition> ::= "if" "(" <logic_expression> ")" <statements> "end_if" """
        self.eat('ID', 'if')
        self.eat('LPAREN')
        self.logic_expression()
        self.eat('RPAREN')
        self.statements()
        self.eat('ID', 'end_if')

    def loop(self):
        """ <loop> ::= "loop" "(" <identifier> "=" <expression> ":" <expression> ")" <statements> "end_loop" """
        self.eat('ID', 'loop')
        self.eat('LPAREN')
        self.eat('ID')
        self.eat('ASSIGN')
        self.expression()
        self.eat('OP', ':')
        self.expression()
        self.eat('RPAREN')
        self.statements()
        self.eat('ID', 'end_loop')

    def logic_expression(self):
        """ <logic_expression> ::= <identifier> <logic_op> <identifier> """
        self.eat('ID')
        self.eat('LOGIC_OP')
        self.eat('ID')

    def expression(self):
        """ Handle arithmetic expressions recursively. """
        self.term()
        while self.current_token and self.current_token[0] == 'OP' and self.current_token[1] in ['+', '-']:
            self.advance()
            self.term()

    def term(self):
        """ <term> ::= <factor> { ("*" | "/" | "%") <factor> } """
        self.factor()
        while self.current_token and self.current_token[0] == 'OP' and self.current_token[1] in ['*', '/', '%']:
            self.advance()
            self.factor()

    def factor(self):
        """ <factor> ::= <number> | <identifier> | "(" <expression> ")" """
        if self.current_token[0] == 'NUMBER':
            self.advance()
        elif self.current_token[0] == 'ID':
            self.advance()
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            self.expression()
            self.eat('RPAREN')
        else:
            raise ParserError("Expected number, identifier, or expression", self.current_token)

    def eat(self, token_type, token_value=None):
        """ Consume a token of the expected type and optional value. """
        if self.current_token and self.current_token[0] == token_type and (token_value is None or self.current_token[1] == token_value):
            self.advance()
        else:
            expected = f"{token_type}='{token_value}'" if token_value else token_type
            raise ParserError(f"Expected {expected}", self.current_token)

# Example usage:
if __name__ == "__main__":
    code = """
    program
    value = 32;
    end_program
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = RecursiveDescentParser(tokens)
    parser.parse()
