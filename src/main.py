from example.app.main import MainApplication

# TODO: Separación claras entre partes de la aplicación: core, apis, others
# TODO: Implementación librerias de proyecto: async events, logging, watchdog
# TODO: Actualizar el ejemplo para incluir nuevas características del framework
# TODO: Mejorar el ejemplo incluyendo: interaction, persistence y performance
if __name__ == "__main__":
    app = MainApplication()
    app.main_loop()
