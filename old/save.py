import os
import sys
import re

from pyparsing import *

def grammar():

    class InvalidArgumentException(ParseFatalException):
        def __init__(self, s, loc, msg):
            super(InvalidArgumentException, self).__init__(
                    s, loc, "invalid argument '%s'" % msg)

    def error(exceptionClass):
        def raise_exception(s,l,t):
            raise exceptionClass(s,l,t[0])
        return Word(alphas,alphanums).setParseAction(raise_exception)

    
    ParserElement.setDefaultWhitespaceChars(" \t")

    #Chaîne de caractères " "
    STR = Regex(r'\"[^\n]*\"')
    #Numérique
    NUM = Regex(r'[0-9]+')
    ARG = Regex(r'\S+')

    #Commentaire
    COM = Regex(r'^#.*$')
    #Espace
    SEP = White(' ', min=1).suppress()
    #Fin de ligne
    EOL = lineEnd.suppress()

    t_emptyLine = lineEnd()
    t_comment = COM.suppress()
    
    #Arguments
    t_args_list = ARG + ZeroOrMore(SEP + ARG)
    t_args_table = Literal('[') + ARG + Literal(']')

    #Séparateur multilignes
    continuation = '\\' + lineEnd()
    t_args_list.ignore(continuation)

    


    #FROM Instruction
    t_from_instruction = Group(Literal('FROM') + SEP + ARG + EOL)
    #MAINTAINER 
    t_maintainer_instruction = Group(Literal('MAINTAINER') + SEP + ARG + EOL)
    #RUN Instruction
    t_run_instruction = Group(Literal('RUN') + SEP + t_args_list + EOL)
    #Expose Instruction
    t_expose_instruction = Group(Literal('EXPOSE') + SEP + NUM + EOL)
    #ADD Instruction 
    t_add_instruction = Group(Literal('ADD') + SEP)
    #COPY Instruction
    t_copy_instruction = Group(Literal('COPY') + (SEP + ARG) * (2, 2) + EOL)
    #ENTRYPOINT
    t_entrypoint_instruction = Group(Literal('ENTRYPOINT') + SEP)
    #CMD
    t_cmd_instruction = Group(Literal('CMD') + SEP + t_args_list + EOL)
    #VOLUME
    t_volume_instruction = Group(Literal('VOLUME') + SEP)
    #WORKDIR
    t_workdir_instruction = Group(Literal('WORKDIR') + SEP)

    #Instructions list
    t_instruction = t_run_instruction \
                    | t_maintainer_instruction \
                    | t_expose_instruction \
                    | t_add_instruction \
                    | t_copy_instruction \
                    | t_entrypoint_instruction \
                    | t_cmd_instruction \
                    | t_volume_instruction \
                    | t_workdir_instruction \
                    | t_emptyLine.suppress() \
                    | t_comment.suppress()

    dockerfile = t_from_instruction + OneOrMore(t_instruction)

    return dockerfile

if os.path.exists('Dockerfile'):

    r = grammar().parseFile('Dockerfile')


    print(r)


