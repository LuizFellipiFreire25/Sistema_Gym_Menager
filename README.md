ProGymManager

📌 Sobre o Projeto

O *ProGymManager* é um sistema de gestão para academias, desenvolvido como um projeto pessoal com foco na organização e automação de processos administrativos. O objetivo é criar uma solução eficiente para o gerenciamento de alunos, funcionários, planos, pagamentos e presença na academia.

O projeto está sendo desenvolvido de forma modular, permitindo escalabilidade e futuras implementações, como um sistema de controle de acesso via QR Code ou reconhecimento facial.

---

🚀 Funcionalidades (em desenvolvimento)

🔹 Gerenciamento Administrativo (Módulo *Administrador.py*)

- Cadastro e gerenciamento de usuários (alunos e funcionários);
- Registro de pagamentos e controle de mensalidades;
- Criação e gerenciamento de planos de treino;
- Visualização e edição de informações de alunos.

🔹 Gerenciamento de Alunos (Módulo *Aluno.py*)

- Acesso ao plano de treino cadastrado;
- Visualização do histórico de pagamentos;
- Registro de presença na academia;
- Notificações sobre vencimento de planos.

🔹 Controle de Acesso e Login (Módulo *Main.py*)

- Interface inicial para login e cadastro;
- Redirecionamento para módulos específicos conforme o tipo de usuário (Aluno ou Administrador).

---

🛠 Estrutura do Projeto

O código está sendo organizado de forma modular:


/ProGymManager
│-- main.py         # Módulo principal para login e autenticação
│-- administrador.py  # Funcionalidades administrativas
│-- aluno.py        # Funcionalidades específicas para alunos (em desenvolvimento)
│-- planos.txt      # Arquivo contendo os planos disponíveis na academia
│-- data/           # Pasta para armazenar dados e registros


Essa estrutura modular facilita futuras expansões, permitindo integração com bancos de dados e interfaces gráficas no futuro.

---

📅 Status do Projeto

O sistema ainda está em desenvolvimento e novas funcionalidades serão adicionadas gradativamente. As principais prioridades no momento são:

- Finalizar o módulo de *Alunos*;
- Melhorar a estrutura do banco de dados;
- Implementar um controle mais robusto de autenticação e permissões.

Este projeto será atualizado conforme novas funcionalidades forem implementadas.

---

👤 Autor

O *ProGymManager* está sendo desenvolvido por Luiz, com o objetivo de aprimorar habilidades em programação e construir uma solução funcional e escalável para academias. 
---

🔗 *Fique ligado para novas atualizações!*
