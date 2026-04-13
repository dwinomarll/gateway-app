import SwiftUI

struct BuddyPanel: View {
    @EnvironmentObject var vm: AppViewModel

    var body: some View {
        VStack(spacing: 0) {
            // Message list
            ScrollViewReader { proxy in
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 8) {
                        ForEach(vm.messages) { msg in
                            ChatBubble(message: msg)
                                .id(msg.id)
                        }
                        if vm.isSending {
                            HStack {
                                ProgressView().scaleEffect(0.7)
                                Text("Buddy is thinking…")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            .padding(.horizontal)
                        }
                    }
                    .padding()
                }
                .onChange(of: vm.messages.count) { _ in
                    if let last = vm.messages.last {
                        withAnimation { proxy.scrollTo(last.id, anchor: .bottom) }
                    }
                }
            }

            Divider()

            // Input bar
            HStack(spacing: 8) {
                TextField("Ask Buddy…", text: $vm.chatInput, axis: .vertical)
                    .textFieldStyle(.plain)
                    .lineLimit(1...4)
                    .onSubmit { Task { await vm.sendMessage() } }

                Button {
                    Task { await vm.sendMessage() }
                } label: {
                    Image(systemName: "arrow.up.circle.fill")
                        .font(.title2)
                        .foregroundColor(vm.chatInput.isEmpty ? Color.secondary : Color.blue)
                }
                .buttonStyle(.plain)
                .disabled(vm.chatInput.isEmpty || vm.isSending)
            }
            .padding(10)
            .background(.bar)
        }
    }
}

struct ChatBubble: View {
    let message: ChatMessage

    var body: some View {
        HStack {
            if message.isUser { Spacer(minLength: 40) }
            Text(message.content)
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(message.isUser ? Color.blue : Color(nsColor: .controlBackgroundColor))
                .foregroundColor(message.isUser ? .white : .primary)
                .clipShape(RoundedRectangle(cornerRadius: 12))
            if !message.isUser { Spacer(minLength: 40) }
        }
    }
}
