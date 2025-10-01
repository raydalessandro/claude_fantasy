# Claude Fantasy 🎭

Una chat di gruppo interattiva dove un umano orchestra conversazioni tra due AI (Claude di Anthropic e DeepSeek), scegliendo chi deve rispondere in ogni momento.

## 🎯 Concept

Claude Fantasy permette conversazioni a tre dove:
- **L'umano** è il moderatore e partecipante
- - **Claude (Anthropic)** - IA conversazionale avanzata
  - - **DeepSeek** - IA con approccio tecnico e analitico
   
    - L'umano decide chi deve rispondere, creando dinamiche conversazionali uniche e controllate.
   
    - ## ✨ Features
   
    - - 🎪 **Multi-AI Chat**: Orchestrazione di conversazioni con più modelli AI
      - - 🧠 **Memoria Persistente**: Context management per coerenza nel tempo
        - - 🎮 **Controllo Turni**: L'umano sceglie chi deve parlare
          - - 💾 **Storico Conversazioni**: Salvataggio e ripristino delle sessioni
            - - 🎨 **UI Intuitiva**: Interfaccia web moderna e responsive
              - - 🔐 **API Key Management**: Gestione sicura delle credenziali
               
                - ## 🛠️ Tecnologie
               
                - - **Backend**: Python/FastAPI o Node.js/Express
                  - - **Frontend**: React/Next.js o Vue.js
                    - - **AI APIs**:
                      -   - Anthropic Claude API
                          -   - DeepSeek API
                              - - **State Management**: Context window optimization
                                - - **Database**: SQLite/PostgreSQL per persistenza
                                 
                                  - ## 📋 Prerequisiti
                                 
                                  - ```bash
                                    # API Keys necessarie
                                    ANTHROPIC_API_KEY=your_anthropic_key
                                    DEEPSEEK_API_KEY=your_deepseek_key
                                    ```

                                    ## 🚀 Quick Start

                                    ```bash
                                    # Clone repository
                                    git clone https://github.com/raydalessandro/claude_fantasy.git
                                    cd claude_fantasy

                                    # Install dependencies
                                    npm install
                                    # oppure
                                    pip install -r requirements.txt

                                    # Configura le API keys
                                    cp .env.example .env
                                    # Modifica .env con le tue chiavi

                                    # Avvia l'applicazione
                                    npm run dev
                                    # oppure
                                    python main.py
                                    ```

                                    ## 📁 Struttura Progetto

                                    ```
                                    claude_fantasy/
                                    ├── backend/
                                    │   ├── api/
                                    │   │   ├── anthropic_client.py
                                    │   │   └── deepseek_client.py
                                    │   ├── services/
                                    │   │   ├── chat_orchestrator.py
                                    │   │   └── memory_manager.py
                                    │   └── main.py
                                    ├── frontend/
                                    │   ├── components/
                                    │   │   ├── ChatInterface.jsx
                                    │   │   └── AISelector.jsx
                                    │   └── app.js
                                    ├── config/
                                    │   └── .env.example
                                    └── README.md
                                    ```

                                    ## 🎮 Come Funziona

                                    1. **Avvia una conversazione**: L'umano scrive un messaggio iniziale
                                    2. 2. **Scegli chi risponde**: Seleziona Claude o DeepSeek
                                       3. 3. **L'AI risponde**: Il modello selezionato genera la risposta
                                          4. 4. **Continua la conversazione**: Ripeti scegliendo quale AI coinvolgere
                                             5. 5. **Memoria contestuale**: Tutte le AI vedono l'intera conversazione
                                               
                                                6. ## 🧩 Accorgimenti per Coerenza
                                               
                                                7. - **Rolling Context Window**: Gestione intelligente del contesto
                                                   - - **Token Budget Management**: Ottimizzazione uso token
                                                     - - **Conversation Summarization**: Riassunti automatici per thread lunghi
                                                       - - **State Persistence**: Salvataggio punti chiave della conversazione
                                                        
                                                         - ## 🔮 Roadmap
                                                        
                                                         - - [ ] Implementazione base chat a 3
                                                           - [ ] - [ ] Integrazione Anthropic API
                                                           - [ ] - [ ] Integrazione DeepSeek API
                                                           - [ ] - [ ] UI/UX frontend
                                                           - [ ] - [ ] Sistema di memoria persistente
                                                           - [ ] - [ ] Export conversazioni
                                                           - [ ] - [ ] Modalità "auto" (AI decidono tra loro i turni)
                                                           - [ ] - [ ] Supporto per più AI (OpenAI, Gemini, etc.)
                                                           - [ ] - [ ] Analytics e insights sulle conversazioni
                                                          
                                                           - [ ] ## 🤝 Contribuire
                                                          
                                                           - [ ] Contributi, issues e feature requests sono benvenuti!
                                                          
                                                           - [ ] ## 📄 Licenza
                                                          
                                                           - [ ] MIT License - vedi [LICENSE](LICENSE)
                                                          
                                                           - [ ] ## 👨‍💻 Autore
                                                          
                                                           - [ ] **raydalessandro**
                                                          
                                                           - [ ] ---
                                                          
                                                           - [ ] *"Where human curiosity meets artificial intelligence"* ✨
