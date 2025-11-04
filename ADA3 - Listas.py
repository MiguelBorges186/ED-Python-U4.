import tkinter as tk
from tkinter import messagebox, simpledialog



class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nombre):
        nuevo = NodoIngrediente(nombre)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.eliminar_repetidos()

    def eliminar(self, nombre):
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.nombre.lower() == nombre.lower():
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def mostrar(self):
        ingredientes = []
        actual = self.cabeza
        while actual:
            ingredientes.append(actual.nombre)
            actual = actual.siguiente
        return ingredientes

    def eliminar_repetidos(self):
        """Elimina todos los ingredientes duplicados automáticamente."""
        vistos = set()
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.nombre.lower() in vistos:
                anterior.siguiente = actual.siguiente
            else:
                vistos.add(actual.nombre.lower())
                anterior = actual
            actual = actual.siguiente


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaIngredientes()


class ListaPostres:
    def __init__(self):
        self.postres = []

    def buscar_postre(self, nombre):
        for postre in self.postres:
            if postre.nombre.lower() == nombre.lower():
                return postre
        return None

    def alta_postre(self, nombre, ingredientes):
        if self.buscar_postre(nombre):
            messagebox.showwarning("Advertencia", f"El postre '{nombre}' ya existe.")
            return
        nuevo = Postre(nombre)
        for ing in ingredientes:
            nuevo.ingredientes.agregar(ing)
        self.postres.append(nuevo)
        self.postres.sort(key=lambda p: p.nombre.lower())
        self.eliminar_repetidos()

    def baja_postre(self, nombre):
        for i, postre in enumerate(self.postres):
            if postre.nombre.lower() == nombre.lower():
                del self.postres[i]
                return True
        return False

    def agregar_ingrediente(self, nombre_postre, ingrediente):
        postre = self.buscar_postre(nombre_postre)
        if not postre:
            return False
        postre.ingredientes.agregar(ingrediente)
        return True

    def eliminar_ingrediente(self, nombre_postre, ingrediente):
        postre = self.buscar_postre(nombre_postre)
        if not postre:
            return None
        return postre.ingredientes.eliminar(ingrediente)

    def eliminar_repetidos(self):
        """Subprograma automático: limpia postres e ingredientes repetidos."""
        nombres_vistos = set()
        nuevos_postres = []
        for postre in self.postres:
            if postre.nombre.lower() not in nombres_vistos:
                postre.ingredientes.eliminar_repetidos()
                nombres_vistos.add(postre.nombre.lower())
                nuevos_postres.append(postre)
        self.postres = nuevos_postres




class App:
    def __init__(self, root):
        self.root = root
        self.root.title(" Gestor de Postres")
        self.root.geometry("600x500")
        self.root.config(bg="#f7f7f7")

        self.lista = ListaPostres()

        tk.Label(root, text="Gestor de Postres", font=("Segoe UI", 18, "bold"), bg="#f7f7f7").pack(pady=10)
        self.text_area = tk.Text(root, width=70, height=18, bg="#fff", relief="ridge", borderwidth=2)
        self.text_area.pack(padx=10, pady=10)

        frame = tk.Frame(root, bg="#f7f7f7")
        frame.pack(pady=5)

        tk.Button(frame, text=" Alta Postre", command=self.alta_postre, width=15, bg="#d1f0c4").grid(row=0, column=0, padx=5, pady=3)
        tk.Button(frame, text=" Baja Postre", command=self.baja_postre, width=15, bg="#f7c4c4").grid(row=0, column=1, padx=5, pady=3)
        tk.Button(frame, text=" Agregar Ingrediente", command=self.agregar_ingrediente, width=18, bg="#c4e1f7").grid(row=1, column=0, padx=5, pady=3)
        tk.Button(frame, text=" Eliminar Ingrediente", command=self.eliminar_ingrediente, width=18, bg="#f9d5a7").grid(row=1, column=1, padx=5, pady=3)
        
        tk.Button(root, text="Actualizar Vista", command=self.mostrar_estructura, bg="#dddddd").pack(pady=5)

        self.mostrar_estructura()

    

    def mostrar_estructura(self):
        self.text_area.delete(1.0, tk.END)
        if not self.lista.postres:
            self.text_area.insert(tk.END, "No hay postres registrados.")
            return
        for postre in self.lista.postres:
            ingredientes = postre.ingredientes.mostrar()
            cadena = f"[{postre.nombre}] → "
            for ing in ingredientes:
                cadena += f"[{ing}] → "
            cadena += "NIL\n"
            self.text_area.insert(tk.END, cadena + "\n")

    def alta_postre(self):
        nombre = simpledialog.askstring("Nuevo Postre", "Nombre del postre:")
        if not nombre:
            return
        ingredientes = simpledialog.askstring("Ingredientes", "Ingresa ingredientes separados por coma:")
        if not ingredientes:
            return
        lista_ing = [i.strip() for i in ingredientes.split(",")]
        self.lista.alta_postre(nombre, lista_ing)
        self.mostrar_estructura()

    def baja_postre(self):
        nombre = simpledialog.askstring("Eliminar Postre", "Nombre del postre a eliminar:")
        if not nombre:
            return
        if self.lista.baja_postre(nombre):
            messagebox.showinfo("Éxito", f"Postre '{nombre}' eliminado.")
        else:
            messagebox.showwarning("Error", f"El postre '{nombre}' no existe.")
        self.mostrar_estructura()

    def agregar_ingrediente(self):
        nombre = simpledialog.askstring("Agregar Ingrediente", "Nombre del postre:")
        if not nombre:
            return
        ingrediente = simpledialog.askstring("Ingrediente", "Ingrediente a agregar:")
        if not ingrediente:
            return
        if self.lista.agregar_ingrediente(nombre, ingrediente):
            messagebox.showinfo("Éxito", f"Ingrediente '{ingrediente}' agregado a {nombre}.")
        else:
            messagebox.showwarning("Error", "El postre no existe.")
        self.mostrar_estructura()

    def eliminar_ingrediente(self):
        nombre = simpledialog.askstring("Eliminar Ingrediente", "Nombre del postre:")
        if not nombre:
            return
        ingrediente = simpledialog.askstring("Ingrediente", "Ingrediente a eliminar:")
        if not ingrediente:
            return
        resultado = self.lista.eliminar_ingrediente(nombre, ingrediente)
        if resultado is None:
            messagebox.showwarning("Error", "El postre no existe.")
        elif resultado:
            messagebox.showinfo("Éxito", f"Ingrediente '{ingrediente}' eliminado.")
        else:
            messagebox.showwarning("Error", "El ingrediente no existe en el postre.")
        self.mostrar_estructura()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
