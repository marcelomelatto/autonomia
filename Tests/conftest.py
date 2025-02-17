import pytest
from tabulate import tabulate
from datetime import datetime

def pytest_terminal_summary(terminalreporter, exitstatus):
    """
    Gera uma tabela detalhada de resultados dos testes e faz append no arquivo de log geral.
    """
    results = []
    log_file = "test_results.log"  # Nome do arquivo de log geral

    # Captura todos os relatórios de testes em uma única estrutura
    all_reports = terminalreporter.stats.get('passed', []) + \
                  terminalreporter.stats.get('failed', []) + \
                  terminalreporter.stats.get('skipped', []) + \
                  terminalreporter.stats.get('error', []) + \
                  terminalreporter.stats.get('xfailed', []) + \
                  terminalreporter.stats.get('xpassed', [])

    # Armazena os resultados únicos
    unique_results = {}
    for report in all_reports:
        key = (report.nodeid, report.when)
        if key not in unique_results:
            unique_results[key] = {
                "filepath": report.location[0],
                "function": report.location[2],
                "passed": 0,
                "failed": 0,
                "error": 0,
                "skipped": 0,
                "xfailed": 0,
                "xpassed": 0
            }

        # Atualiza os contadores com base no status do teste
        if report.passed:
            unique_results[key]["passed"] += 1
        elif report.failed:
            unique_results[key]["failed"] += 1
        elif report.skipped:
            unique_results[key]["skipped"] += 1
        elif report.outcome == "xfailed":
            unique_results[key]["xfailed"] += 1
        elif report.outcome == "xpassed":
            unique_results[key]["xpassed"] += 1

    # Converte os resultados para uma lista
    for data in unique_results.values():
        results.append([
            data["filepath"],
            data["function"],
            data["passed"],
            data["failed"],
            data["error"],
            data["skipped"],
            data["xfailed"],
            data["xpassed"]
        ])

    # Adiciona a linha TOTAL
    totals = [sum(col) for col in zip(*[r[2:] for r in results])]
    results.append(["TOTAL", "", *totals])

    # Gera uma tabela formatada
    table = tabulate(
        results,
        headers=["filepath", "function", "passed", "failed", "error", "skipped", "xfailed", "xpassed"],
        tablefmt="grid",
    )

    # Exibe no terminal
    terminalreporter.section("Test Results")
    terminalreporter.write_line(table)

    # Adiciona os resultados ao arquivo de log geral
    with open(log_file, "a") as f:
        f.write("\n\n")
        f.write(f"Test Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(table)
        f.write("\n")

    print(f"\nResults appended to {log_file}")
