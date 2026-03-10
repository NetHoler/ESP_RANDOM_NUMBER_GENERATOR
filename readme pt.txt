===============================================================================
                       GERADOR DE NÚMEROS ESP (v1.0)
                       Manual do Utilizador & Auditoria
===============================================================================

1. SOBRE O SOFTWARE
-------------------
O Gerador de Números ESP é uma ferramenta de alta precisão desenhada para 
experiências de percepção extra-sensorial, testes de aleatoriedade e sorteios 
profissionais. O foco principal é a integridade dos dados e a imersão do 
utilizador.

2. FLUXO DE CONFIGURAÇÃO
------------------------
Ao iniciar, o programa guia o utilizador através de três etapas:

   [A] IDIOMA: Seleção entre Português (PT) e Inglês (EN).
   [B] TEMPORIZADOR: Define o tempo de espera (1 a 36000 segundos).
       Ideal para períodos de concentração ou meditação pré-sorteio.
   [C] DÍGITOS: Define a extensão do número (1 a 9 algarismos).

   NOTA: Se as caixas de entrada ficarem VERMELHAS, o valor inserido é 
   inválido ou está fora do intervalo permitido.

3. CONTROLOS E ATALHOS
----------------------
A interface foi desenhada para ser minimalista. Pode utilizar os botões 
inferiores ou os seguintes atalhos de teclado:

   [ Esc ] ....... Alternar entre Ecrã Completo / Janela
   [  I  ] ....... Inverter Cores (Modo Escuro / Modo Claro)
   [ Mouse ] ..... Em Ecrã Completo, mova o rato para mostrar a interface

4. SISTEMA DE AUDITORIA (LOGS)
------------------------------
Para garantir que não houve manipulação, todos os resultados são registados 
automaticamente num ficheiro no seu Ambiente de Trabalho (Desktop):
Ficheiro: "esp_audit_logs.txt"

Cada entrada no log contém:
   - TIMESTAMP: Data e hora exata do evento.
   - RESULTADO: O número gerado pelo sistema.
   - SEED (SEMENTE): Valor de nanosegundos (CPU) usado na aleatoriedade.
   - PREPARAÇÃO: Tempo total de sessão até à geração do número.
   - CONFIG: Parâmetros de dígitos e tempo selecionados.

5. CARACTERÍSTICAS TÉCNICAS
---------------------------
* ANTI-SLEEP: O programa impede que o monitor se desligue durante a contagem.
* ESCALAMENTO: O número ajusta o seu tamanho automaticamente para garantir 
  legibilidade máxima em qualquer resolução.
* PRIVACIDADE: O software funciona localmente e não requer ligação à internet.

6. RESOLUÇÃO DE PROBLEMAS
-------------------------
- Os botões desapareceram? 
  No modo Ecrã Completo, a interface oculta-se após 3 segundos para evitar 
  distrações. Mova o rato para que os controlos reapareçam.

- O histórico não abre? 
  Certifique-se de que o ficheiro "esp_audit_logs.txt" no seu Ambiente de 
  Trabalho não está aberto noutro programa que bloqueie a sua leitura.

-------------------------------------------------------------------------------
Desenvolvido para fins de investigação e entretenimento técnico. 2026.
===============================================================================