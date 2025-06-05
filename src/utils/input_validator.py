class InputValidator:
    @staticmethod
    def valida_matricola(matricola: str) -> bool:
        return (matricola and 
                matricola.isdigit() and 
                5 <= len(matricola) <= 10)

    @staticmethod
    def valida_nome(nome: str) -> bool:
        return bool(nome and nome.strip())

    @staticmethod
    def valida_voto(voto: str) -> bool:
        try:
            voto_num = int(voto)
            return 18 <= voto_num <= 30
        except ValueError:
            return False