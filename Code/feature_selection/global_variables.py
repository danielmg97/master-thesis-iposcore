outputs=[
            "dias na UCI",
            "complicação pós-cirúrgica",
            "classificação clavien-dindo",
            "óbito até 1 ano ",
            "dias no  IPOP",
            "óbito_tempo decorrido após data cirurgia (até 1 ano)"
        ] # 6

numericas=[
            "idade",
            # "total pontos NAS",       # POS
            # "pontos NAS por dia",     # POS
            "Score fisiológico P-Possum",
            "Score gravidade cirúrgica P-Possum",
            "% morbilidade P-Possum",
            "% mortalidade P-Possum",
            "ACS altura",
            "ACS peso",
            "complicações sérias (%)",
            "risco médio",
            "qualquer complicação (%)",
            "risco médio.1",
            "pneumonia (%)",
            "risco médio.2",
            "complicações cardíacas (%)",
            "risco médio.3",
            "infeção cirúrgica (%)",
            "risco médio.4",
            "ITU (%)",
            "risco médio.5",
            "tromboembolismo venoso (%)",
            "risco médio.6",
            "falência renal (%)",
            "risco médio.7",
            # "ileus (%)",              # MISSING VALUES
            # "risco médio.8",          # MISSING VALUES
            # "fuga anastomótica (%)",  # MISSING VALUES
            # "risco médio.9",          # MISSING VALUES
            "readmissão (%)",
            "risco médio.10",
            "reoperação (%)",
            "risco médio.11",
            "morte (%)",
            "risco médio.12",
            "Discharge to Nursing or Rehab Facility (%)",
            "risco médio.13",
            "ACS - previsão dias internamento",
            "ARISCAT PONTUAÇÃO TOTAL",
            "SCORE ARISCAT"
            # "PONTOS - Charlson Comorbidity Index", # MISSING VALUES
            # "% Sobrevida estimada em 10 anos"      # MISSING VALUES
            ] # 42 ou 34 efetivas

nominais = [
            "especialidade",
            "LOCALIZAÇÃO ",                         #muito fácil de usar estratégia de bags
            "diagnóstico pré-operatório",
            #"Operação efetuada",                                             # POS
            #"procedimentos_COD",                   #muitos missing           # POS
            #"descrição complicação pós-cirúrgica",                           # POS
            #"complicação_COD",                     #muitos missing           # POS
            # "Informação adicional",               #muitos missing           # POS
            "Comorbilidades pré-operatórias"
        ] # 9 ou 4 efetivas

codigos = [
            #"Intervenções_ICD10",                  # POS
            "ACS_procedimento"
        ] # 2 ou 1 efetiva

categoricas = [
                #"tipo pedido anestesia",           # POS
                #"proveniência",                    # POS
                #"motivo admissão UCI",             # POS
                "tipo cirurgia",
                "especialidade_COD",
                #"destino após UCI",                # POS
                "ASA",
                "PP idade",
                "PP cardíaco",
                "PP respiratório",
                "PP ECG",
                "PP pressão arterial sistólica",
                "PP pulsação arterial",
                "PP hemoglobina",
                "PP leucócitos",
                "PP ureia",
                "PP sódio",
                "PP potássio",
                "PP escala glasglow",
                "PP tipo operação",
                "PP nº procedimentos",
                "PP perda sangue",
                "PP contaminação peritoneal",
                "PP estado da malignidade",
                "PP CEPOD-classificação operação",
                "ACS idade",
                "ACS estado funcional",
                "ACS ASA",
                "ACS sépsis sistémica",
                "ACS diabetes",
                "ACS dispneia",
                "ARISCAT Idade",
                "ARISCAT SpO2 ",
                "ARISCAT incisão cirúrgica",
                "ARISCAT duração cirurgia"
                # "CHARLSON Idade",                                     # MISSING VALUES
                # "CHARLSON Diabetes mellitus",                         # MISSING VALUES
                # "CHARLSON Doença fígado",                             # MISSING VALUES
                # "CHARLSON Malignidade",                               # MISSING VALUES
                #"complicação principal_COD",                           # POS
                #"classificação ACS complicações específicas",          # POS
                #"destino após IPO"                                     # POS
                ] # 42 ou 31 efetivas

binarias = [
            "género",
            "1ª Cirurgia IPO",
            "QT pré-operatória",
            #" reinternamento na UCI",      # POS
            "ACS género",
            "ACS emergência",
            "ACS esteróides",
            "ACS ascite",
            "ACS dependente ventilador",
            "ACS cancro disseminado",
            "ACS hipertensão",
            "ACS ICC",
            "ACS fumador",
            "ACS DPOC",
            "ACS diálise",
            "ACS insuficiência renal aguda",
            "ARISCAT infeção respiratória último mês",
            "ARISCAT anemia pré-operativa",
            "ARISCAT procedimento emergente"
            # "CHARLSON SIDA",
            # "CHARLSON Doença Renal Crónica Moderada a Severa",    # MISSING VALUES
            # "CHARLSON Insuficiência Cardíaca",                    # MISSING VALUES
            # "CHARLSON Enfarte Miocárdio",                         # MISSING VALUES
            # "CHARLSON DPOC",                                      # MISSING VALUES
            # "CHARLSON Doença Vascular periférica",                # MISSING VALUES
            # "CHARLSON AVC ou Ataque Isquémico Transitório",       # MISSING VALUES
            # "CHARLSON Demência",                                  # MISSING VALUES
            # "CHARLSON Hemiplegia",                                # MISSING VALUES
            # "CHARLSON Doença do Tecido Conjuntivo",               # MISSING VALUES
            # "CHARLSON Úlcera Péptica",                            # MISSING VALUES
            #"classificação ACS complicações gerais"                # POS
        ] # 31 ou 18 efetivas

datas = [
            #"data pedido pela anestesia",      # POS
            #"data admissão UCI",               # POS
            "data cirurgia"
            #"data óbito"  # muitos missing     # POS
        ] # 4 ou 1 efetiva