import platform
import subprocess
from django.shortcuts import render
from .models import Url


def home(request):
    return render(request, "home.html")


def search(request):
    alvo = ""
    resultado_ping = None
    sucesso = None

    if request.method == "POST":
        alvo = request.POST.get("name", "").strip()

        if alvo:
            Url.objects.create(name=alvo)

            if platform.system().lower() == "windows":
                comando = ["ping", "-n", "3", "-w", "2000", alvo]
            elif platform.system().lower() == "linux":
                comando = ["ping", "-c", "3", "-W", "2", alvo]
            else:
                comando = ["ping", "-c", "3", "-W", "2000", alvo]

            try:
                proc = subprocess.run(
                    comando,
                    capture_output=True,
                    text=True,
                    timeout=100,
                )
                resultado_ping = proc.stdout or proc.stderr
                sucesso = proc.returncode == 0
            except subprocess.TimeoutExpired:
                resultado_ping = "Demorou demais para responder."
                sucesso = False

    return render(
        request,
        "search.html",
        {
            "alvo": alvo,
            "resultado_ping": resultado_ping,
            "sucesso": sucesso,
        },
    )