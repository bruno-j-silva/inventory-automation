import { useEffect, useState } from "react";
import { getReadiness } from "./shared/api";

type ServiceState = "loading" | "ready" | "unavailable";

export function App() {
  const [state, setState] = useState<ServiceState>("loading");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 8000);
    let active = true;
    getReadiness(controller.signal)
      .then((ready) => {
        if (active) setState(ready ? "ready" : "unavailable");
      })
      .catch(() => {
        if (active) setState("unavailable");
      })
      .finally(() => window.clearTimeout(timeout));
    return () => {
      active = false;
      window.clearTimeout(timeout);
      controller.abort();
    };
  }, [attempt]);

  const labels = {
    loading: "Verificando disponibilidade…",
    ready: "Serviço disponível",
    unavailable: "Serviço indisponível no momento",
  };

  return (
    <div className="shell">
      <a className="skip-link" href="#conteudo">
        Ir para o conteúdo
      </a>
      <header className="header">
        <a className="brand" href="#inicio">
          <span className="brand-mark" aria-hidden="true">
            A
          </span>{" "}
          Inventário de Automações
        </a>
        <nav aria-label="Navegação principal">
          <a href="#inicio">Visão geral</a>
          <a href="#acesso">Acesso</a>
        </nav>
      </header>
      <main id="conteudo">
        <section className="intro" id="inicio">
          <p className="eyebrow">GESTÃO E GOVERNANÇA</p>
          <h1>
            Conheça suas automações.
            <br />
            Cuide de cada processo.
          </h1>
          <p className="lead">
            Um espaço para reunir automações, responsáveis e informações do dia
            a dia da sua organização.
          </p>
        </section>
        <section className="status-panel" aria-labelledby="availability-title">
          <div>
            <h2 id="availability-title">Disponibilidade</h2>
            <p role="status" aria-live="polite" className={`status ${state}`}>
              <span aria-hidden="true">●</span> {labels[state]}
            </p>
          </div>
          <button
            disabled={state === "loading"}
            onClick={() => {
              setState("loading");
              setAttempt((value) => value + 1);
            }}
          >
            Verificar novamente
          </button>
        </section>
        <section
          id="acesso"
          className="access-panel"
          aria-labelledby="access-title"
        >
          <p className="eyebrow">ACESSO À PLATAFORMA</p>
          <h2 id="access-title">O acesso está em preparação.</h2>
          <p>
            O login será disponibilizado nesta página. Ainda não é possível
            entrar ou cadastrar automações.
          </p>
        </section>
      </main>
      <footer>Inventário de Automações · Uso interno</footer>
    </div>
  );
}
