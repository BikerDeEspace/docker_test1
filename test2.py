import os
import sys
import re

from pyparsing import *

def dockerfile_grammar():
    def error(s, loc, expr, err):
        raise ParseFatalException(s, loc, "Erreur de syntaxe au niveau de la ligne {l}".format(l=lineno(loc, s)))

    ParserElement.setDefaultWhitespaceChars(" \t")

    #
    # TERMINAUX
    #
    STR = Regex(r'\"(.*?)\"').setName('chaîne de caractère')
    NUM = Regex(r'[0-9]+').setName('numérique')
    ARG = Regex(r'\S+').setName('argument')
    COM = Regex(r'#.*').setName('Commentaire')
    SEP = White(' ', min=1).suppress().setName('Espace')

    EOL = lineEnd().suppress()
    EL = lineEnd().suppress()

    OH = Literal('[').suppress()
    CH = Literal(']').suppress()
    CO = Literal(',').suppress()

    #
    # NON TERMINAUX
    #
    t_args_table = (OH - STR - (CO - STR) * (0, 3) -  CH).setName('["argument"]')
    t_args_list = ARG - ZeroOrMore(SEP - Optional(ARG))
    #Séparateur multilignes
    continuation = '\\' - lineEnd()
    t_args_list.ignore(continuation)

    t_comment = COM.suppress()
    t_emptyline = EL.suppress()


    #SINGLE ARG INSTRUCTIONS
    #FROM Instruction
    t_from_instruction = Literal('FROM') - SEP - Group(ARG) - EOL
    #VOLUME
    t_volume_instruction = Literal('VOLUME') - SEP - Group(ARG) - EOL
    #WORKDIR
    t_workdir_instruction = Literal('WORKDIR') - SEP - Group(ARG) - EOL
    #MAINTAINER 
    t_maintainer_instruction = Literal('MAINTAINER') - SEP - Group(ARG) - EOL

    #LIST ARG INSTRUCTIONS
    #RUN Instruction
    t_run_instruction = Literal('RUN') - SEP - Group(t_args_table | t_args_list) - EOL
    #CMD
    t_cmd_instruction = Literal('CMD') - SEP - Group(t_args_table | t_args_list) - EOL
    #ENTRYPOINT
    t_entrypoint_instruction = Literal('ENTRYPOINT') - SEP - Group(t_args_table | t_args_list) - EOL


    #ADD Instruction 
    t_add_instruction = Literal('ADD') - Group((SEP - ARG) * (0, 2)) - EOL
    #COPY Instruction
    t_copy_instruction = Literal('COPY') - Group((SEP - ARG) * (0, 2)) - EOL

    #OTHER TYPE
    #Expose Instruction
    t_expose_instruction = Literal('EXPOSE') - SEP - Group(NUM) - EOL

    #Instructions list
    t_instruction =   t_run_instruction \
                    | t_maintainer_instruction \
                    | t_expose_instruction \
                    | t_add_instruction \
                    | t_copy_instruction \
                    | t_entrypoint_instruction \
                    | t_cmd_instruction \
                    | t_volume_instruction \
                    | t_workdir_instruction \
                    | t_emptyline \
                    | t_comment


    #dockerfile grammar 
    dockerfile = stringStart() - ZeroOrMore(t_emptyline | t_comment) - t_from_instruction - ZeroOrMore(t_instruction.setFailAction(error)) - stringEnd()
    
    return dockerfile

if os.path.exists('Dockerfile'):
    try:
        r = dockerfile_grammar().parseFile('Dockerfile')
    except ParseFatalException as e:
        print(e.msg)