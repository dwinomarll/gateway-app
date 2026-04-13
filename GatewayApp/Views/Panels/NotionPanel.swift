import SwiftUI

struct NotionPanel: View {
    @EnvironmentObject var vm: AppViewModel
    @State private var selected: NotionCase?

    var body: some View {
        HSplitView {
            // Case list
            List(vm.cases, selection: $selected) { c in
                VStack(alignment: .leading, spacing: 2) {
                    Text(c.merchant)
                        .font(.subheadline)
                        .lineLimit(1)
                    Text(c.status)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
                .tag(c)
                .padding(.vertical, 2)
            }
            .listStyle(.sidebar)
            .frame(minWidth: 180, maxWidth: 240)

            // Detail
            if let c = selected {
                VStack(alignment: .leading, spacing: 12) {
                    Text(c.merchant)
                        .font(.title2.bold())
                    Text("Status: \(c.status)")
                        .foregroundStyle(.secondary)
                    if let f = c.followUpDate {
                        Text("Follow-up: \(f)")
                            .font(.caption)
                    }
                    Spacer()
                }
                .padding()
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
            } else {
                ContentUnavailableView("Select a case", systemImage: "doc.text")
            }
        }
        .toolbar {
            ToolbarItem {
                Button { Task { await vm.refreshCases() } } label: {
                    Image(systemName: "arrow.clockwise")
                }
            }
        }
    }
}
