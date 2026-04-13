import SwiftUI

struct PanelContainer<Content: View>: View {
    let title:   String
    let icon:    String
    @ViewBuilder let content: () -> Content
    @State private var collapsed = false

    var body: some View {
        VStack(spacing: 0) {
            // Header bar
            HStack {
                Label(title, systemImage: icon)
                    .font(.headline)
                    .foregroundStyle(.primary)
                Spacer()
                Button {
                    withAnimation(.easeInOut(duration: 0.2)) { collapsed.toggle() }
                } label: {
                    Image(systemName: collapsed ? "chevron.right" : "chevron.down")
                        .imageScale(.small)
                }
                .buttonStyle(.plain)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(.bar)

            Divider()

            if !collapsed {
                content()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
