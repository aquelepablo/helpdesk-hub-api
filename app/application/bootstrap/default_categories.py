DEFAULT_CATEGORIES: list[dict[str, str | bool]] = [
    {
        "name": "Acesso a Sistemas",
        "description": (
            "Solicitações de login, senha, permissões e desbloqueio de acesso."
        ),
        "is_active": True,
    },
    {
        "name": "Hardware",
        "description": "Problemas com notebook, desktop, monitor e periféricos.",
        "is_active": True,
    },
    {
        "name": "Software / Sistemas Internos",
        "description": "Erros, falhas e duvidas em sistemas e aplicações internas.",
        "is_active": True,
    },
    {
        "name": "Rede e Conectividade",
        "description": "Problemas com internet, Wi-Fi, VPN e acesso remoto.",
        "is_active": True,
    },
    {
        "name": "Email e Comunicação",
        "description": (
            "Dificuldades com email corporativo, ferramentas de "
            "comunicação e colaboração."
        ),
        "is_active": True,
    },
    {
        "name": "Operacional / Suporte Interno",
        "description": (
            "Solicitações de suporte relacionadas a processos internos, "
            "infraestrutura e ambiente de trabalho."
        ),
        "is_active": True,
    },
]
