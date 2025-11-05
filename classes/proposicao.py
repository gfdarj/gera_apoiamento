from dataclasses import dataclass
from docx.oxml import parse_xml
from docx.shared import Pt
from urllib.parse import urlparse


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
        if (
            "PROJETO" in self.tipo_proposicao.upper()
            and "LEI" in self.tipo_proposicao.upper()
            and "COMPL" in self.tipo_proposicao.upper()
        ):
            tipo_resumido = "PLC"
            tipo = "Projeto de Lei Complementar"
        else:
            if "PROJETO" in self.tipo_proposicao.upper() and "LEI" in self.tipo_proposicao.upper():
                tipo_resumido = "PL"
                tipo = "Projeto de Lei"

        return tipo_resumido if nome_resumido else tipo

    # ---------- Função corrigida ----------
    def add_hyperlink(self, paragraph, text, url):
        """
        Adiciona um hyperlink ao parágrafo do Word (apenas no trecho 'text').
        Corrige o erro de namespace 'r' e adiciona esquema http/https se faltar.
        """
        # Garante que a URL tenha esquema
        if not url.lower().startswith(("http://", "https://")):
            url = "https://" + url

        part = paragraph.part
        r_id = part.relate_to(
            url,
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
            is_external=True
        )

        hyperlink_xml = (
            f'<w:hyperlink r:id="{r_id}" '
            f'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            f'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        )
        hyperlink = parse_xml(hyperlink_xml)

        # Texto do link
        new_run = paragraph.add_run(text)
        new_run.font.underline = True
        new_run.font.size = Pt(12)

        hyperlink.append(new_run._r)
        paragraph._p.append(hyperlink)

        return hyperlink
