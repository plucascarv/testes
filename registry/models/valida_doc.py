import re

def validate_cnpj(self, cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        # Primeiro dígito verificador
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        r = soma % 11
        d1 = 0 if r < 2 else 11 - r
        if int(cnpj[12]) != d1:
            return False
        # Segundo dígito verificador
        pesos2 = [6] + pesos1  # [6,5,4,3,2,9,8,7,6,5,4,3,2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        r = soma % 11
        d2 = 0 if r < 2 else 11 - r
        return int(cnpj[13]) == d2



def validate_cpf(self, cpf: str) -> bool:
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        # Primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        if int(cpf[9]) != d1:
            return False
        # Segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        return int(cpf[10]) == d2
    