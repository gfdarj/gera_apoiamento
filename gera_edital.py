import classes.aplicacao
from classes.planilha import PlanilhaProjetos

print("Teste de execução")
P = PlanilhaProjetos()
print("Carregando projetos")
p = P.CarregaColunas()
print(f"Projetos selecionados: {len(p)}")

if len(p) > 0:
    dados_ordenados = sorted(p, key=lambda x: (x.relator, int(x.ano), int(x.numero)))

for d in dados_ordenados:
    print(f"relator: {d.relator}  ------ numero:{d.numero}/{d.ano}  ----- EP? {d.emenda_de_plenario}")


