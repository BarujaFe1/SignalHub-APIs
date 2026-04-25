# SignalHub APIs - Índice de Documentação

**Última Atualização**: 2026-04-25 16:13 UTC

---

## 📋 Início Rápido

**Novo no projeto?** Comece aqui:
1. Leia [`STATUS.md`](STATUS.md) - Estado atual em 2 minutos
2. Execute `start.bat` - Inicia backend + frontend
3. Acesse http://localhost:3001 - Veja o sistema funcionando

---

## 📚 Documentação Principal

### Para Desenvolvedores
- **[DEVELOPER.md](DEVELOPER.md)** - Guia completo do desenvolvedor
  - Comandos úteis
  - Estrutura do projeto
  - Troubleshooting
  - Configuração

### Para Gestão/Overview
- **[STATUS.md](STATUS.md)** - Estado atual do projeto (TL;DR)
- **[README.md](README.md)** - Visão geral e arquitetura
- **[SUMMARY.md](SUMMARY.md)** - Resumo executivo detalhado

### Para Continuidade Técnica
- **[PLAN.md](PLAN.md)** - Plano de desenvolvimento (V4)
- **[VALIDATION.md](VALIDATION.md)** - Relatório de validação
- **[SESSION_REPORT.md](SESSION_REPORT.md)** - Relatório da sessão de continuidade

---

## 🛠️ Scripts Úteis

### Validação
```bash
cd apps/api
venv\Scripts\activate

# Validar todos os endpoints
python validate_api.py

# Inspecionar banco de dados
python inspect_db.py
python inspect_data.py

# Testar queries
python test_queries.py
```

### Execução Manual
```bash
# Executar todos os conectores
python trigger_connectors.py

# Executar conector específico
python trigger_weather.py
```

### Inicialização
```bash
# Iniciar tudo (Windows)
start.bat

# Iniciar apenas backend
start_api.bat
```

---

## 📊 Estado Atual (2026-04-25)

| Componente | Status | Detalhes |
|------------|--------|----------|
| Backend API | ✅ Funcional | 8 endpoints validados |
| Frontend | ✅ Funcional | Rodando em :3001 |
| Database | ✅ Funcional | 19 runs, 62 signals |
| Conectores | ✅ Funcional | 3/3 executando |
| Scheduler | ⏳ Pendente | Configurado, não testado |

---

## 🎯 Próximos Passos

### Imediato
1. [ ] Validar scheduler com backend rodando
2. [ ] Capturar screenshots do frontend
3. [ ] Atualizar README com screenshots

### Curto Prazo
1. [ ] Configurar PostgreSQL
2. [ ] Adicionar monitoring (Sentry)
3. [ ] Setup CI/CD
4. [ ] Deploy staging

---

## 📁 Estrutura de Arquivos

```
signalhub-apis/
├── 📄 STATUS.md              ← Comece aqui (estado atual)
├── 📄 DEVELOPER.md           ← Guia do desenvolvedor
├── 📄 VALIDATION.md          ← Relatório de validação
├── 📄 SESSION_REPORT.md      ← Relatório da sessão
├── 📄 SUMMARY.md             ← Resumo executivo
├── 📄 PLAN.md                ← Plano de desenvolvimento
├── 📄 README.md              ← Visão geral do projeto
├── 📄 INDEX.md               ← Este arquivo
│
├── 🚀 start.bat              ← Iniciar tudo
├── 🚀 start_api.bat          ← Iniciar apenas backend
│
├── apps/
│   ├── api/                  ← Backend FastAPI
│   │   ├── app/              ← Código da aplicação
│   │   ├── alembic/          ← Migrations
│   │   ├── venv/             ← Virtual environment
│   │   ├── signalhub.db      ← Database SQLite
│   │   ├── validate_api.py   ← Script de validação
│   │   ├── trigger_connectors.py ← Executar conectores
│   │   ├── inspect_db.py     ← Inspecionar schema
│   │   └── inspect_data.py   ← Inspecionar dados
│   │
│   └── web/                  ← Frontend Next.js
│       ├── src/              ← Código fonte
│       └── package.json      ← Dependências
│
├── packages/
│   └── ingestion/            ← Pipeline de dados
│       ├── connectors/       ← Conectores de API
│       ├── jobs/             ← Job runner
│       └── quality/          ← Quality checks
│
└── docs/                     ← Documentação adicional
```

---

## 🔍 Encontrar Informação Rápida

### "Como eu inicio o projeto?"
→ [`STATUS.md`](STATUS.md) seção "Como Usar"

### "Quais comandos estão disponíveis?"
→ [`DEVELOPER.md`](DEVELOPER.md) seção "Common Tasks"

### "O que está funcionando?"
→ [`VALIDATION.md`](VALIDATION.md) seção "Validation Results"

### "O que foi feito na última sessão?"
→ [`SESSION_REPORT.md`](SESSION_REPORT.md)

### "Qual o próximo passo?"
→ [`PLAN.md`](PLAN.md) seção "Execution Phases"

### "Como funciona a arquitetura?"
→ [`README.md`](README.md) seção "Architecture"

### "Quais são os problemas conhecidos?"
→ [`VALIDATION.md`](VALIDATION.md) seção "Known Issues"

---

## 🆘 Troubleshooting Rápido

### Backend não inicia
```bash
cd apps/api
venv\Scripts\activate
set PYTHONPATH=C:\dev\signalhub-apis\apps\api;C:\dev\signalhub-apis
python -c "from app.main import app; print('OK')"
```

### Frontend não inicia
```bash
cd apps/web
npm install
npm run dev
```

### Conectores falhando
```bash
cd apps/api
venv\Scripts\activate
python trigger_connectors.py
```

### Banco de dados com problemas
```bash
cd apps/api
venv\Scripts\activate
python inspect_db.py
```

---

## 📞 Suporte

1. Consulte [`DEVELOPER.md`](DEVELOPER.md) para comandos
2. Consulte [`VALIDATION.md`](VALIDATION.md) para issues conhecidos
3. Consulte [`SESSION_REPORT.md`](SESSION_REPORT.md) para contexto

---

## ✅ Checklist de Validação

Use este checklist para validar o sistema:

- [ ] Backend inicia sem erros
- [ ] Frontend inicia sem erros
- [ ] `/health` retorna status healthy
- [ ] `/api/v1/sources` retorna 3 sources
- [ ] Frontend mostra dados reais
- [ ] Conectores executam manualmente
- [ ] Dados persistem no banco
- [ ] Quality checks passam
- [ ] Freshness está atualizado

---

## 📈 Métricas de Sucesso

```
✅ Backend: 8/8 endpoints funcionando
✅ Frontend: 5/5 páginas funcionando
✅ Conectores: 3/3 executando
✅ Database: 7/7 tabelas criadas
✅ Quality: 100% pass rate
⏳ Scheduler: Configurado (não testado)
```

---

**Projeto**: SignalHub APIs  
**Status**: ✅ Funcional  
**Última Validação**: 2026-04-25 16:13 UTC
