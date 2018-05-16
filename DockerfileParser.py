#pyparsing imports
from pyparsing import ParserElement, ParseFatalException
from pyparsing import Literal, Group, Regex, White, ZeroOrMore, Optional, lineno
from pyparsing import stringStart, stringEnd, lineStart, lineEnd

class DockerfileParser:
    def __init__(self):
        """DockerfileParser Class Constructor
   
        Check & Verify the syntax of a Dockerfile type file

        """
        self.error = list()
        self.grammar = self.dockerfile_grammar()


    def hasError(self):
        """hasError
        
        Return True if errors
        
        """
        if self.error:
            return True
        else:
            return False

    def parse(self, FilePath='./', Filename = 'Dockerfile'):
        """Parse
        
        Parsing of a Dockerfile file
        
        Params :
        FilePath -- Dockerfile directory (./ by default)
        Filename -- Dockerfile filename (Dockerfile by default)

        """
        self.error = list()
        self.file = FilePath + Filename

        try:
            r = self.grammar.parseFile(self.file)
            self.fileparsed = r
        except ParseFatalException as e:
            self.error.append(e.msg)

    def dockerfile_grammar(self):
        """Dockerfile grammar
        
        Define the grammar of a Dockerfile 

        """

        def error(s, loc, expr, err):
            """TODO Improve error messages"""


            print()
            error = "Erreur de syntaxe au niveau de la ligne {l}".format(l=lineno(loc, s))
            raise ParseFatalException(s, loc, error)

        #INIT
        ParserElement.setDefaultWhitespaceChars(" \t")

        #
        # TERMINALS
        #
        STR = Regex(r'\"(.*?)\"').setName('chaîne de caractère')
        NUM = Regex(r'[0-9]+').setName('numérique')
        ARG = Regex(r'\S+').setName('argument')
        COM = Regex(r'#.*').setName('Commentaire')
        SEP = White(' ', min=1).suppress().setName('Espace')

        EOL = lineEnd().suppress()
        EL  = lineEnd().suppress()

        OH = Literal('[').suppress()
        CH = Literal(']').suppress()
        CO = Literal(',').suppress()

        #
        # NO TERMINALS
        #
        #Arguments
        t_args_table = OH - STR - (CO - STR) * (0, 3) -  CH
        t_args_list = ARG - ZeroOrMore(SEP - Optional(ARG))
        #Multiple lines separator
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
        t_add_instruction = Literal('ADD') - Group((SEP - ARG) * (2, 2)) - EOL
        #COPY Instruction
        t_copy_instruction = Literal('COPY') - Group((SEP - ARG) * (2, 2)) - EOL

        #OTHER TYPE
        #Expose Instruction
        t_expose_instruction = Literal('EXPOSE') - SEP - Group(NUM) - EOL

        #Instructions list
        t_instruction =   t_from_instruction \
                        | t_run_instruction \
                        | t_maintainer_instruction \
                        | t_expose_instruction \
                        | t_add_instruction \
                        | t_copy_instruction \
                        | t_entrypoint_instruction \
                        | t_cmd_instruction \
                        | t_volume_instruction \
                        | t_workdir_instruction \

        #Comment / Empty lines
        t_other = t_emptyline \
                | t_comment

        #Grammaire complète
        dockerfile = stringStart() - ZeroOrMore(t_other | Group(t_instruction)) - stringEnd()
        
        return dockerfile