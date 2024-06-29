#!/usr/bin/python3

html = open('email_templates/welcome.html').read()
edited = html.replace("to", "in")
print(edited)