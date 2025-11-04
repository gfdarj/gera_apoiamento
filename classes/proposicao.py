from dataclasses import dataclass
from docx.oxml import parse_xml
from docx.shared import Pt
#from docx import Document
#from docx.oxml.ns import qn

'''
Classe Proposicao - Classe base para as proposições.
'''
@dataclass
class Proposicao:
    ordem: int = 0
    numero: str = ''
    ano: str = ''
    tipo_proposicao: str = ''
    ementa: str = ''
    texto: str = ''
    reuniao: str = ''
    relator: str = ''
    autores: str = None
    parecer: str = None
    emenda_de_plenario: bool = False
    linha_da_planilha: int = None


    def classifica_tipo_proposicao(self, nome_resumido=False):
        if "PROJETO" in self.tipo_proposicao.upper() and "LEI" in self.tipo_proposicao.upper() and "COMPL" in self.tipo_proposicao.upper():
            tipo_resumido = "PLC"
            tipo = "Projeto de Lei Complementar"
        else:
            if "PROJETO" in self.tipo_proposicao.upper() and "LEI" in self.tipo_proposicao.upper():
                tipo_resumido = "PL"
                tipo = "Projeto de Lei"

        if nome_resumido:
            return tipo_resumido
        else:
            return tipo


    def add_hyperlink(paragraph, text, url):
        """
        Adiciona um hyperlink a um parágrafo do Word.
        """
        # Obter o objeto de relacionamento
        part = paragraph.part
        r_id = part.relate_to(
            url,  # destino
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
            is_external=True
        )

        # Criar o elemento <w:hyperlink>
        hyperlink = parse_xml(f'<w:hyperlink r:id="{r_id}" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"></w:hyperlink>')

        # Criar o texto que será exibido
        new_run = paragraph.add_run(text)
        new_run.font.color.rgb = None  # cor padrão do tema
        new_run.font.underline = True
        new_run.font.size = Pt(12)

        # Anexar o run dentro da tag <w:hyperlink>
        hyperlink.append(new_run._r)
        paragraph._p.append(hyperlink)

        return hyperlink

