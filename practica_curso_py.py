saldo_inicial = int(input("cuanto dinero tienes inicialmente "))

def gastos_iniciales():
    trasnporte = int(input("cuanto gastas en trasporte"))
    comida = int(input("cuanto gastas en comida?"))
    material = int(input("cuanto gastas en materiales??"))
    gastos_totales = trasnporte + comida + material
    return gastos_totales

dinero_restante = saldo_inicial - gastos_iniciales()

if dinero_restante > 0:
    print(f"te queda dinero bien hecho, tu saldo restante es: {dinero_restante}")

if dinero_restante == 0:
    print(f"no te queda dinero ya ahorra masss!! tu dinero restante es:{dinero_restante}")

if dinero_restante < 0:
    print(f"estas en deunda pidele a mexdin!! tu dinero restante es: {dinero_restante}")