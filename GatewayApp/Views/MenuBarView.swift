import SwiftUI

struct MenuBarView: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Health row
            HStack {
                Text("GATEWAY")
                    .font(.headline)
                Spacer()
                Circle()
                    .fill(vm.healthColor)
                    .frame(width: 10, height: 10)
                Text(vm.health?.summary ?? "connecting…")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Divider()

            // Last 3 cases
            if vm.cases.isEmpty {
                Text("No active cases")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            } else {
                ForEach(vm.cases.prefix(3)) { c in
                    HStack {
                        Text(c.merchant)
                            .font(.caption)
                            .lineLimit(1)
                        Spacer()
                        Text(c.status)
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                    }
                }
            }

            Divider()

            Button("Open GATEWAY") {
                NSApp.activate(ignoringOtherApps: true)
            }
            .buttonStyle(.plain)
            .font(.caption)
        }
        .padding(12)
        .frame(width: 260)
    }
}
