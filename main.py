import argparse
from app.CmdApp import CmdApp

parser = argparse.ArgumentParser()

group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-f", "--fields", help="Available fields", action="store_true")
group2.add_argument("-F", "--formats", help="Available formats", action="store_true")

subparsers = parser.add_subparsers(help='commands')

search_parser = subparsers.add_parser('search', help='search in data')
search_parser.set_defaults(which='search')
search_parser.add_argument("base", help="Select the database")
search_parser.add_argument("keyword", help="Search keyword in the database")

cli_parser = subparsers.add_parser('cli', help='start the interactive command line')
cli_parser.set_defaults(which='cli')
cli_parser.add_argument("-b", "--base", help="Select the database")

import_parser = subparsers.add_parser('import', help='import into the database')
import_parser.set_defaults(which='import')
import_parser.add_argument("base", help="Select the database")
import_parser.add_argument("fileimport", help="Import file to the database")

export_parser = subparsers.add_parser('export', help="Export from the database")
export_parser.set_defaults(which='export')
export_parser.add_argument("base", help="Select the database")
export_parser.add_argument("to", help="Output file")
export_parser.add_argument("-s", "--select-contact", help="Select contacts by id")
export_parser.add_argument("-z", "--zip", help="zip if more than one out file", action="store_true")

list_parser = subparsers.add_parser('display', help="Display contacts")
list_parser.set_defaults(which='list')
list_parser.add_argument("base", help="Select the database")
list_parser.add_argument("-s", "--select-contact", help="Select contacts by id")

web_parser = subparsers.add_parser("web", help="Start the web service")
web_parser.set_defaults(which='web')
web_parser.add_argument("base", help="Select the database")
web_parser.add_argument("-p", "--port", help="Custom port for web interface", type=int)
web_parser.add_argument("-ip", "--ip-address", help="Ip to bind")

convert_parser = subparsers.add_parser('convert', help='Convert data')
convert_parser.set_defaults(which='convert')
convert_parser.add_argument("-f", "--from", help="Input file to convert")
convert_parser.add_argument("-t", "--to", help="Output file after convert")
convert_parser.add_argument("-z", "--zip", help="zip if more than one out file", action="store_true")


contact_parser = subparsers.add_parser('contact', help='Manage contact')
contact_parser.set_defaults(which='contact')
contact_parser.add_argument("base", help="Select the database")
group = contact_parser.add_mutually_exclusive_group()
group.add_argument("-a", "--add", help="Add a contact", action="store_true")
group.add_argument("-e", "--edit", help="Edit the selected contact")
group.add_argument("-d", "--delete", help="Delete the selected contact")

clear_parser = subparsers.add_parser('clear', help='clear database')
clear_parser.add_argument("base", help="Select the database")
clear_parser.set_defaults(which='clear')

args = parser.parse_args()

print(args)

if not CmdApp.parse(args):
    parser.print_help()
