# test 1 = testa se arg1 está vazio, aceita label.
def test1(testvar, label=""):
    def logictest(var):
        if var == "":
            return True
        else:
            return False
    
    if label: # quer retorno
        if logictest(testvar):
            return print(f"[{label}] Sem conteúdo.")
        else:
            return print(f"[{label}] Há conteúdo. ({testvar})")
    else:
        return logictest(testvar)
        
# test 2 = testa se arg1 é igual a arg2, aceita label
def test2(testvar, comparator, label=""):
    def logictest(var):
        if var == comparator:
            return True
        else:
            return False
    
    if label: # quer retorno
        if logictest(testvar):
            return print(f"[{label}] Igual.")
        else:
            return print(f"[{label}] Diferente.")
    else:
        return logictest(testvar)
    
# Para redirecionar à outro path da URL
def redirectTo(path, *args, **kwargs):
    try: 
        msg=kwargs['mensagem']
    except KeyError:
        pass # Não importa se passar a mensagem ou não.
    
    # debug para consultar se o redirectTo está recebendo os argumentos
    #print(f"args: {args}") 
    #print(f"kwargs: {kwargs}")
    return f'<script>window.location.assign("{path}")</script>'