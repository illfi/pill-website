import flask
import os

app = flask.Flask(__name__)
app.secret_key = "pill_interpreter"
app.debug = True


class Example():
    name = ""
    code = ""
    output = ""
    pretty_name = ""

    def __init__(self, pretty, name, code, output):
        self.name = name
        self.code = code
        self.output = output
        self.pretty_name = pretty
    
class Type():
    name = ''
    description = ''

    def __init__(self, name, desc):
        self.name = name
        self.description = desc

class OpCode():
    name = ''
    arguments = ''
    description = ''

    def __init__(self, name, args, desc):
        self.name = name
        self.arguments = args
        self.description = desc

def get_opcodes():
    opcodes = []
    opcodes.append(OpCode('mov', '[num / container] -> [container]', 'Move an integer literal into a container.'))
    
    opcodes.append(OpCode('mod', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of modulus (%) on the first two arguments.'))
    opcodes.append(OpCode('gt', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of (>) on the first two arguments.'))
    opcodes.append(OpCode('lt', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of (<) on the first two arguments.'))
    opcodes.append(OpCode('gte', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of (>=) on the first two arguments.'))
    opcodes.append(OpCode('lte', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of (<=) on the first two arguments.'))
    opcodes.append(OpCode('eq', '[num / container] -> [num / container] -> [string]', 'Create a variable with the result of (==) on the first two arguments.'))
    
    opcodes.append(OpCode('mvv', '[num / container] -> [variable]', 'Copy an the contents of a container into a variable.'))
    opcodes.append(OpCode('mak', '[string] -> [int]', 'Create a instruction scoped variable with a default value.'))
    opcodes.append(OpCode('dis', '[container]', 'Output the data of the container to STDOUT.'))
    opcodes.append(OpCode('dsl', '[container]', 'Output the data of the container to STDOUT with a newline.'))
    opcodes.append(OpCode('pt', '[string]', 'Output a string to STDOUT.'))
    opcodes.append(OpCode('ptl', '[string]', 'Output a string to STDOUT with a newline.'))
    opcodes.append(OpCode('do',  '[instruction]', 'Execute another instruction'))
    opcodes.append(OpCode('dor',  '[instruction] -> [string]', 'Execute another instruction and save the result to a variable.'))
    opcodes.append(OpCode('neg',  '[container]', 'Invert the (truthy) side of the variable. Equal to (!).'))
    opcodes.append(OpCode('for',  '[string] -> [num] -> [num] -> [num] -> [instruction[', 'Create a for loop, creating a variable with the first argument, to, from and step are the next three, and a reference to the instruction as the last.'))
    opcodes.append(OpCode('del', '[variable]', 'Delete a variable from the scope (Useful for helper methods that require additional variables'))
    opcodes.append(OpCode('if', '[opcode_result] -> [instruction] -> [instruction]', 'Evaluate the result then execute either the first instruction if true, or the second if false.')) 
    return opcodes

def get_types():
    types = []
    types.append(Type('num', 'A number, (f64) in rust.'))
    types.append(Type('string', 'A string'))
    types.append(Type('container', 'A reference to the container by name. Containers can either be variables or registers.'))
    types.append(Type('register', 'A reference to one of the global registers by name.'))
    types.append(Type('variable', 'A reference to one of the local (instruction scoped) registers.'))
    types.append(Type('instruction', 'A reference to an instruction defined BEFORE the parent instruction.'))
    types.append(Type('num / container', 'Parsed as either a number or a container reference, but always evaluated as the value.'))
    return types

def get_examples():
    def load_example(filename):
        print('filename={}'.format(filename))
        file = os.path.join(os.getcwd(), 'static', 'examples', filename, '{}.ill'.format(filename))
        with open(file, 'r') as f:
            return f.read()

    def load_example_output(filename):
        file = os.path.join(os.getcwd(), 'static', 'examples', filename, '{}_output.txt'.format(filename))
        with open(file, 'r') as f:
            return f.read()

    examples = []
    
    ex = [('Hello World', 'hello_world'), 
          ('Empty File', 'empty_file'),
          ('FizzBuzz', "fizzbuzz")]
    for ext in ex:
        (p, f) = ext
        out = load_example_output(f)
        print(out.replace('\n', '\\n'))
        examples.append(Example(p, f, load_example(f), out.replace('\n', '\\n')))

    #examples.append(Example('Empty File', 'empty_file', '+a;\n\n$$ () {\n}', ''))
    #examples.append(Example('Creating Variables', 'creating_variables', '+a;\n\n$$ () {\n\tmak b 1;\n\tdis b;\n}', 'b = 1'))
    #examples.append(Example('Creating Variables', 'creating_variables', '+a;\n\n$$ () {\n\tmak b 1;\n\tdis b;\n}', 'b = 1'))
    return examples

def get_rules():
    rules = []
    rules.append('Pill files MUST have at least one register.')
    rules.append('Pill files MUST have at least one instruction. If it is not the main function ($$), then the first function found will be designated as main.')
    rules.append('To escape containers that shadow global ones, use quotes like, so "b" instead of b, otherwise you are allowed to use the name without quotes.')
    return rules


@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html')

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/docs')
def docs():
    return flask.render_template('documentation.html', rules=get_rules(), examples=get_examples(), types=get_types(), opcodes=get_opcodes())