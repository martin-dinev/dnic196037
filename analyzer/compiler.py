import json
import sys
from itertools import takewhile

IOSTREAM_LINE = "#include <iostream>"
BRACKETS = {"{": "}", "(": ")"}
MULTI_CHARS_OPERATORS = ("++", "--", "==", "<=", ">=", "+=", "-=", "*=", "/=", "%=")
SINGLE_CHAR_OPERATORS = ("-", "+", "*", "/", "%", ">", "<", ";", "=")
EXPRESSION_TERMINATORS = (";", ",", ")")

OPERATORS = {
    "leading_unary_operators": ("++", "--"),
    "trailing_unary_operators": ("++", "--"),
    "assignment_operators": ("=", "+=", "-=", "*=", "/=", "%="),
    "first_operators": ("*", "/", "%"),
    "second_operators": ("+", "-"),
    "boolean_operators": ("<=", ">=", ">", "<", "=="),
}


class MyException(Exception):
    pass


def parse_code(code):  # returns (success, message, runnable)
    success, tokens_or_message = tokenize(code)
    if not success:
        message = tokens_or_message
        return False, message, []
    tokens = tokens_or_message

    for token in tokens:
        if token[:2] == "//":
            code = code[:code.find(token)] + code[code.find(token) + len(token):]
    tokens = list(filter(lambda t: not t[:2] == "//", tokens))

    if tokens[0] != IOSTREAM_LINE:
        return False, "first line must be '#include <iostream>'", []
    if tokens[1:5] != ["using", "namespace", "std", ";"]:
        return False, "second line must be 'using namespace std;'", []
    if tokens[5:9] != ["int", "main", "(", ")"]:
        return False, "third line must be 'int main()'", []
    if tokens[9] != "{":
        return False, "'int main()' must be followed by '{'", []

    line = 0
    code_pos = 0

    def increment_line(fragment):
        nonlocal line, code_pos, code, tokens
        tokens = tokens[tokens.index(fragment) + 1:]
        fragment_position = code.find(fragment, code_pos)
        line += code[code_pos:fragment_position].count('\n')
        code_pos = fragment_position + len(fragment)
        return line

    def move_line():
        nonlocal line, code_pos, code
        fragment_position = code.find(tokens[0], code_pos)
        line += code[code_pos:fragment_position].count('\n')
        code_pos = fragment_position
        return line

    increment_line(IOSTREAM_LINE)
    increment_line(";")  # using namespace std ->;<-
    increment_line(")")  # int main( ->)<-

    variable_names = []
    scope_variables_counts = []

    def is_active_variable(var_name):
        return var_name[0].isalpha() and var_name.isalnum() and var_name in variable_names

    def compile_expression_from_tokens(expression_tokens):
        expression_size = len(expression_tokens)
        expression = {"kind": "expression", "exec": dict(), "line": line}
        data = expression["exec"]
        if expression_size == 0:
            raise MyException("don't know what to do with empty expression")
        elif expression_size == 1:
            if expression_tokens[0].isnumeric():
                data["kind"] = "number"
                data["value"] = int(expression_tokens[0])
            elif is_active_variable(expression_tokens[0]):
                data["kind"] = "variable_access"
                data["name"] = expression_tokens[0]
            else:
                raise MyException("was expecting a number or a declared variable name")
        elif expression_size == 2:
            if expression_tokens[0] in OPERATORS["leading_unary_operators"]:
                if is_active_variable(expression_tokens[1]):
                    data["kind"] = "leading_unary"
                    data["sub"] = expression_tokens[0]
                    data["name"] = expression_tokens[1]
                else:
                    raise MyException(
                        "was expecting a declared variable name after unary operator " + expression_tokens[0])
            elif expression_tokens[1] in OPERATORS["trailing_unary_operators"]:
                if is_active_variable(expression_tokens[0]):
                    data["kind"] = "trailing_unary"
                    data["sub"] = expression_tokens[1]
                    data["name"] = expression_tokens[0]
                else:
                    raise MyException(
                        "was expecting a declared variable name before unary operator " + expression_tokens[1])
            else:
                raise MyException("was expecting a unary operator and a declared variable name")
        else:
            top_level = []
            level = 0
            level_zero_tokens = 0
            latest_first = -1
            latest_second = -1
            assignment_present = False

            for i, token in enumerate(expression_tokens):
                if token == "(":
                    level += 1
                elif token == ")":
                    if level == 0:
                        raise MyException("no matching '(' for ')'")
                    level -= 1
                elif level == 0:
                    level_zero_tokens += 1
                    if token in OPERATORS["assignment_operators"]:
                        assignment_present = True
                        if i == 1 and is_active_variable(expression_tokens[0]):
                            data["kind"] = "assignment"
                            data["sub"] = expression_tokens[1]
                            data["name"] = expression_tokens[0]
                            data["value"] = compile_expression_from_tokens(expression_tokens[2:])
                        else:
                            raise MyException(
                                "was expecting a declared variable name before assignemnt operator " + token)
                        break
                    elif token in OPERATORS["second_operators"]:
                        latest_second = i
                    elif token in OPERATORS["first_operators"]:
                        latest_first = i
                    else:
                        if not is_active_variable(token) and not token.isnumeric():
                            raise MyException("I don't understand the token " + token)

            if not assignment_present:
                if latest_second != -1:
                    if latest_second == 0 or latest_second == len(expression_tokens) - 1:
                        raise MyException(
                            "binary operator " + expression_tokens[latest_second] + " should have two operands")
                    else:
                        data["kind"] = "binary"
                        data["sub"] = expression_tokens[latest_second]
                        data["left"] = compile_expression_from_tokens(expression_tokens[0:latest_second])
                        data["right"] = compile_expression_from_tokens(expression_tokens[latest_second + 1:])
                elif latest_first != -1:
                    if latest_first == 0 or latest_first == len(expression_tokens) - 1:
                        raise MyException(
                            "binary operator " + expression_tokens[latest_first] + " should have two operands")
                    else:
                        data["kind"] = "binary"
                        data["sub"] = expression_tokens[latest_first]
                        data["left"] = compile_expression_from_tokens(expression_tokens[0:latest_first])
                        data["right"] = compile_expression_from_tokens(expression_tokens[latest_first + 1:])
                elif level_zero_tokens == 0:
                    expression = compile_expression_from_tokens(expression_tokens[1:-1])
                else:
                    raise MyException("need an operator in non unary expressions")

        return expression

    def compile_condition_from_tokens(condition_tokens):
        condition_size = len(condition_tokens)
        condition = {"kind": "condition", "exec": dict(), "line": line}
        data = condition["exec"]
        if condition_size == 0:
            raise MyException("don't know what to do with empty condition")
        else:
            level = 0
            level_zero_tokens = 0
            found = -1

            for i, token in enumerate(condition_tokens):
                if token == "(":
                    level += 1
                elif token == ")":
                    if level == 0:
                        raise MyException("no matching '(' for ')'")
                    level -= 1
                elif level == 0:
                    level_zero_tokens += 1
                    if token in OPERATORS["assignment_operators"]:
                        raise MyException("return value of assignment operators is not boolean")
                    if token in OPERATORS["boolean_operators"]:
                        if found == -1:
                            found = i
                        else:
                            raise MyException("more than one boolean operators found")

            if found != -1:
                if found == 0 or found == len(condition_tokens) - 1:
                    raise MyException(
                        "binary operator " + condition_tokens[found] + " should have two operands")
                else:
                    data["kind"] = "boolean"
                    data["sub"] = condition_tokens[found]
                    data["left"] = compile_expression_from_tokens(condition_tokens[0:found])
                    data["right"] = compile_expression_from_tokens(condition_tokens[found + 1:])
            elif level_zero_tokens == 0:
                condition = compile_expression_from_tokens(condition_tokens[1:-1])
            else:
                raise MyException("need an operator in non unary expressions")

        return condition

    def compile_expression():
        level = 0

        def should_terminate(ind, t):
            nonlocal level
            if tokens[ind] == '(':
                level += 1
            elif tokens[ind] == ')':
                level -= 1
            return t in EXPRESSION_TERMINATORS and (t != ")" or level == -1)

        expression_size = next(i for i, t in enumerate(tokens) if should_terminate(i, t))
        expression_tokens = tokens[:expression_size]
        move_line()
        compiled_expression = compile_expression_from_tokens(expression_tokens)
        for i in range(expression_size):
            increment_line(tokens[0])
        return compiled_expression

    def compile_condition():
        level = 0

        def should_terminate(ind, t):
            nonlocal level
            if tokens[ind] == '(':
                level += 1
            elif tokens[ind] == ')':
                level -= 1
            return t in EXPRESSION_TERMINATORS and (t != ")" or level == -1)

        condition_size = next(i for i, t in enumerate(tokens) if should_terminate(i, t))
        condition_tokens = tokens[:condition_size]
        move_line()
        compiled_condition = compile_condition_from_tokens(condition_tokens)
        for i in range(condition_size):
            increment_line(tokens[0])
        return compiled_condition

    def compile_variable_declaration():
        result = {"kind": "new_int", "exec": dict(), "line": -1}
        result["exec"]["name"] = tokens[0]
        result["line"] = increment_line(tokens[0])

        if tokens[0] == "=":
            increment_line("=")
            result["exec"]["undefined"] = False
            result["exec"]["value"] = compile_expression()
        else:
            result["exec"]["undefined"] = True
            result["exec"]["value"] = None
        return result

    def compile_element():
        result = {"kind": "", "exec": [], "line": -1}
        if tokens[0] == "int":
            result["kind"] = "declaration"
            result["line"] = increment_line("int")
            while tokens[0] != ";":
                element = compile_variable_declaration()
                variable_names.append(element["exec"]["name"])
                scope_variables_counts[-1] += 1
                result["exec"].append(element)
                if tokens[0] == ",":
                    increment_line(",")
            increment_line(";")
        elif tokens[0] == "for":
            result["kind"] = "for"
            result["line"] = increment_line("(")

            scope_variables_counts.append(0)

            result["exec"].append(compile_element())
            result["exec"].append(compile_condition())
            increment_line(";")
            result["exec"].append(compile_expression())
            increment_line(")")
            result["exec"].append(compile_scope())

            while scope_variables_counts[-1] > 0:
                scope_variables_counts[-1] -= 1
                variable_names.pop()
            scope_variables_counts.pop()
        elif tokens[0] == "if":
            result["kind"] = "if"
            result["line"] = increment_line("(")
            result["exec"].append(compile_condition())
            increment_line(")")
            result["exec"].append(compile_scope())
        elif tokens[0] == "while":
            result["kind"] = "while"
            result["line"] = increment_line("(")
            result["exec"].append(compile_condition())
            increment_line(")")
            result["exec"].append(compile_scope())
        else:
            result = compile_expression()
            increment_line(";")

        return result

    def compile_scope():
        result = {"kind": "scope", "exec": [], "line": -1}

        scope_variables_counts.append(0)

        if tokens[0] == "{":
            result["line"] = increment_line("{")
            while tokens[0] != "}":
                element = compile_element()
                result["exec"].append(element)
            increment_line("}")
        else:
            result["line"] = move_line()
            result["exec"].append(compile_element())

        while scope_variables_counts[-1] > 0:
            scope_variables_counts[-1] -= 1
            variable_names.pop()
        scope_variables_counts.pop()

        return result

    try:
        compiled_code = compile_scope()
    except MyException as e:
        return False, "line " + str(line + 1) + ":" + str(e) + "\n" \
               " It appears somewhere before: " + " ".join(tokens[:10]), []

    compiled_code = json.dumps(compiled_code)

    if len(tokens) != 0:
        return False, "there must not be code out of main scope", compiled_code

    return True, "compiled successfully", compiled_code


def next_token(code):
    once = False
    while not once or (len(code) > 0 and code[0] == '\n'):
        once = True
        if len(code) > 0 and code[0] == "\n":
            code = code[1:]
        code = code.lstrip()

    if len(code) == 0:
        return True, None

    if code[0].isalpha():
        return True, "".join(takewhile(lambda ch: ch.isalnum() or ch == "_", code))

    if code[0].isnumeric():
        return True, "".join(takewhile(lambda ch: ch.isnumeric(), code))

    if code[0] == "#":
        incl = "#include <iostream>"
        if code[:len(incl)] == incl:
            return True, "#include <iostream>"
        else:
            return False, "# can only include iostream"

    if code[:2] in MULTI_CHARS_OPERATORS:
        return True, code[:2]

    if code[:2] == "//":
        return True, code[0:code.find("\n")]

    if code[0] in SINGLE_CHAR_OPERATORS + (",",):
        return True, code[0]

    if code[0] in BRACKETS.keys():
        count = 1
        pos = 1
        while count > 0:
            new_pos_open = code.find(code[0], pos)
            new_pos_close = code.find(BRACKETS[code[0]], pos)
            if new_pos_open != -1 and new_pos_open < new_pos_close:
                count += 1
                pos = new_pos_open + 1
            elif new_pos_close == -1:
                return -1, code[0] + " missing a closing bracket"
            else:
                count -= 1
                pos = new_pos_close + 1
        return True, code[0]

    if code[0] in BRACKETS.values():
        return True, code[0]

    return False, "I have never seen " + code[0]


def tokenize(code):
    tokens = []
    while True:
        success, token_or_message = next_token(code)
        if success:
            token = token_or_message
            if token is None:
                break
            tokens.append(token)
            code = code[code.index(token) + len(token):]
        else:
            message = token_or_message
            return False, message
    return True, tokens
