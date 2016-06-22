import re
import sys

create_pattern = re.compile(r"create table (.*) \(", re.I)
output = "DELIMITER //\n\n"
table = None
parameters = []

for line in map(lambda line: line.strip().rstrip(","), sys.stdin):
    match = create_pattern.match(line)
    if match:
        table = match.group(1)
        output += "CREATE PROCEDURE insert" + table + "("
    elif table:
        if line == ");":
            parameter_names = ", ".join(map(lambda parameter: parameter[0], parameters))
            output += ", ".join(map(lambda parameter: " ".join(parameter), parameters)) + ")\n"
            output += "\tBEGIN\n"
            output += "\t\tINSERT INTO " + table + " ("
            output += parameter_names + ") VALUES ("
            output += parameter_names + ");\n"
            output += "\tEND//\n\n"
            table = None
            del parameters[:]
        elif not re.match("(primary)|(foreign) key .*", line, re.I) and not re.match(".* auto_increment.*", line, re.I):
            split = line.split(" ")
            parameters.append((split[0], split[1]))

print(output + "DELIMITER ;")
