#!/usr/bin/python3
#
# by Siddharth Dushantha 2023
#
import requests
import json
import jwt
import sys
import argparse
import re
from utils.printer import Printer
import xml.etree.ElementTree as ET
from utils.msapi import MSAPI
import os.path

printer = Printer(color=True, verbose=False)

def indent(paragraph:str, spaces:int = 2):
    lines = paragraph.split('\n')
    indented_lines = [f"{' '*spaces}{line}" for line in lines]
    indented_paragraph = '\n'.join(indented_lines)
    return indented_paragraph

def json_to_formatted_text(json_data: dict) -> str:
    """
    Convert JSON data to a nicely opinionated text
    
    Args:
        json_data (dict): JSON data that should be formatted
        
    Returns:
        str: The formatted text
        
    Example:
        If the following is the input:
          {
              "name": "Bob"
              "age": 100
              "hobbies": ["golf", "walking", "swimming"]
          }
    
        This function will return the following:
          name    : Bob
          age     : 100
          hobbies : ["golf", "walking", "swimming"]
    """
    formatted_text = ""
    longest = len(max(json_data.keys(), key=len))
    for key, value in json_data.items():
        formatted_text += f"{key:<{longest+1}}: {value}\n"
    return formatted_text.rstrip("\n")


def recon(target, jwt_file):
    if "@" in target:
        if not jwt_file:
            printer.negative("Please provide a Microsoft Teams JWT token with by using the '--jwt' flag")
            sys.exit()
            
        try:
            with open(jwt_file) as f:
                token = f.read().strip()
        except FileNotFoundError:
            printer.negative(f"{jwt_file} could not be found")
            sys.exit()
            
        ms_api = MSAPI(token, target)
        user_data = ms_api.get_user_data()
        
        if not user_data:
            printer.negative(f"{target} does not exist in Azure AD or Microsoft Office 365")
            sys.exit(1)
            
        user_presence = ms_api.get_user_presence(user_data["mri"])
        # Appending 'user_presence' to 'user_data' so that the json_to_formatted_text() output
        # is aligned for both data. If we have them separately the alignment will be wrong
        user_data = dict(list(user_data.items()) + list(user_presence.items()))
        
        printer.positive(target)
        printer.content(json_to_formatted_text(user_data))

    else:
        ms_api = MSAPI()
        tenant_info = ms_api.get_tenant_info(target)
        printer.positive(target)
        
        longest = len(max(tenant_info.keys(), key=len))
        for item in tenant_info:
            printer.content(f"{item:<{longest+1}}: {tenant_info[item]}") 

def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument(
        "-j",
        "--jwt",
        metavar="PATH",
        help="Path to file containing your Microsoft Teams JWT token",
    )

    parser.add_argument(
        "-t",
        "--target",
        metavar="TARGET",
        help="Email address or domain you'd like to fetch information for",
    )

    parser.add_argument(
        "-l",
        "--list",
        metavar="FILE",
        help="File containing email addresses or domains you'd like to fethc information for",
    )
    
    args = parser.parse_args()

    jwt_file = args.jwt
    target = args.target
    target_list = args.list
     
    
    if target:
        recon(target, jwt_file)

 
    if target_list:
        try:
            with open(target_list) as f:
                targets = f.readlines()
                for target in targets:
                    target = target.strip()
                    recon(target.strip(), jwt_file)
                    print()
        except FileNotFoundError:
            printer.negative(f"The file '{target_list}' can not be found")
            
main()