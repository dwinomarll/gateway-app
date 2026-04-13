import SwiftUI

struct GmailPanel: View {
    var body: some View {
        ContentUnavailableView {
            Label("Gmail", systemImage: "envelope.badge.slash")
        } description: {
            Text("Gmail integration coming in Phase 2.")
                .foregroundStyle(.secondary)
        }
    }
}
