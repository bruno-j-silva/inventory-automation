import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { App } from "./App";

describe("Disponibilidade", () => {
  it("exibe indisponibilidade e permite recuperar após nova consulta", async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(new Response(JSON.stringify({ status: "ready" })));
    vi.stubGlobal("fetch", fetchMock);
    render(<App />);
    expect(screen.getByRole("status")).toHaveTextContent("Verificando");
    expect(
      await screen.findByText("Serviço indisponível no momento"),
    ).toBeInTheDocument();
    fireEvent.click(
      screen.getByRole("button", { name: "Verificar novamente" }),
    );
    expect(await screen.findByText("Serviço disponível")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("não informa disponibilidade para resposta com formato inesperado", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValue(new Response(JSON.stringify({ status: "unknown" }))),
    );
    render(<App />);
    expect(
      await screen.findByText("Serviço indisponível no momento"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "O acesso está em preparação." }),
    ).toBeInTheDocument();
  });
});
