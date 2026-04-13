import SwiftUI

struct MainWindowView: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        HStack(spacing: 0) {
            PanelContainer(title: "Notion", icon: "doc.text") {
                NotionPanel()
            }
            Divider()
            PanelContainer(title: "Buddy", icon: "bubble.left.and.bubble.right") {
                BuddyPanel()
            }
            Divider()
            PanelContainer(title: "Gmail", icon: "envelope") {
                GmailPanel()
            }
        }
        .environmentObject(vm)
        .onAppear { vm.boot() }
        .frame(minWidth: 900, minHeight: 560)
        .background(.background)
    }
}
