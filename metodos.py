import simpy
import random
import string
import flet as ft





def main(page: ft.Page):
    page.title = "Teoria de colas"
    txt_number = ft.TextField(
            width=700,
            multiline=True,
            min_lines=3,
            max_lines=20,
            disabled=False,
            text_align=ft.TextAlign.CENTER,
            bgcolor="white",
            color="black",
            border_radius=100,
            )
    
    
    log=[]

    class Cliente:
        def __init__(self, letra, prioridad):
            self.letra = letra
            self.prioridad = prioridad

    def llegada(env, sistema):
        while True:
            yield env.timeout(random.expovariate(7/5)) 
            prioridad = random.randint(1, 3)  # Generar una prioridad aleatoria entre 1 y 3
            letra = obtener_letra_aleatoria(sistema)  # Obtener una letra aleatoria que no esté en uso
            cliente = Cliente(letra=letra, prioridad=prioridad)
            sistema.append(cliente)
            log.append(f"Llegó un cliente {cliente.letra} con prioridad {cliente.prioridad} en el tiempo {env.now}")

    def obtener_letra_aleatoria(sistema):
        letras_disponibles = [letra for letra in string.ascii_uppercase if letra not in [cliente.letra for cliente in sistema]]
        return random.choice(letras_disponibles)

    def atencion(env, sistema):
        while True:
            if sistema:
                sistema.sort(key=lambda x: x.prioridad, reverse=True)  # Ordenar la lista de clientes por prioridad (mayor a menor)
                cliente = sistema.pop(0)  # Tomar al cliente de más alta prioridad
                log.append(f"Atendiendo al cliente {cliente.letra} con prioridad {cliente.prioridad} en el tiempo {env.now}")
                yield env.timeout(1)  # Tiempo de atención de 1 unidad
                log.append(f"Cliente {cliente.letra} atendido en el tiempo {env.now}")
            else:
                yield env.timeout(1)  # Esperar 1 unidad si no hay clientes en la cola

    def actualizar_lista(env, sistema):
        while True:
            if sistema:
                log.append("Lista de clientes restantes por atender:")
                clientes_esperando = [f"{cliente.letra}:{cliente.prioridad}" for cliente in sistema]
                log.append(clientes_esperando)
            yield env.timeout(1)  # Actualizar la lista cada segundo

    def iniciar_simulacion():
        # Simulación
        env = simpy.Environment()
        sistema = []
        env.process(llegada(env, sistema))
        env.process(atencion(env, sistema))
        env.process(actualizar_lista(env, sistema))
        env.run(until=10)  # Duración de la simulación
        

    

    def button_click(e):
        txt_number.value = ""
        log.clear()
        iniciar_simulacion()
        update_text()
        page.update()

    def update_text():
        txt_number.value = "\n".join(str(event) for event in log)


        
    page.add(
        ft.SafeArea(
            ft.Row(
                [
                    ft.Text("Orden de prioridad", style=ft.TextStyle(size=30, weight="bold")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,

            )

        ),
        ft.Row(
            [
            ft.ElevatedButton(
                text="Empezar simulacion",
                on_click=button_click,
                width=200,
                bgcolor="blue",
                color="white",
                ),
            ],
              alignment=ft.MainAxisAlignment.CENTER,

            ),
            ft.Row(
            [
            txt_number,
            ],
             alignment=ft.MainAxisAlignment.CENTER,
            ),

    )

ft.app(main)
