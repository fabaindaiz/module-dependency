from dependency.cli import loader

if __name__ == "__main__":
    print(loader.load_provider(
        module=loader.Module(
            name="Module",
            path="src.plugin.module",
        ),
        component=loader.Component(
            name="Interface",
            interface="Interface",
            methods=["method1", "method2", "method3"],
        ),
        provider=loader.Provider(
            name="InterfaceA",
            imports=["interface1", "interface2"],
        ),
    ))