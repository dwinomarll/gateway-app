import SwiftUI

@main
struct GatewayApplication: App {
    @StateObject private var vm = AppViewModel()

    var body: some Scene {
        MenuBarExtra {
            MenuBarView().environmentObject(vm)
        } label: {
            MenuBarLabel().environmentObject(vm)
        }
        .menuBarExtraStyle(.window)

        WindowGroup("GATEWAY") {
            MainWindowView().environmentObject(vm)
        }
        .defaultSize(width: 1100, height: 680)
        .commands { CommandGroup(replacing: .newItem) {} }
    }
}
